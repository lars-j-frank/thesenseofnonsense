export async function onRequest(context) {
    const { env, request } = context;
    const url = new URL(request.url);
    
    // Get token from either query param (from auth redirect) or environment variable
    let token = url.searchParams.get('access_token') || env.GITHUB_TOKEN;
    const provider = url.searchParams.get('provider') || 'github';
    
    // Clean the token
    if (token) {
        token = token.trim();
    }
    
    if (!token || token === 'undefined' || token === '') {
        return new Response('Missing or invalid access token', { 
            status: 400,
            headers: { 'Content-Type': 'text/plain' }
        });
    }

    // Send the token back to the opener window (the Decap CMS admin interface)
    const html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Authentication Successful</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 2rem; }
    </style>
</head>
<body>
    <p>Authentication successful!</p>
    <p>This window will close automatically.</p>
    
    <script>
        // Function to send authentication data to the opener window
        function sendAuthData() {
            if (!window.opener || window.opener.closed) {
                // If opener is not available, try again after a short delay
                setTimeout(sendAuthData, 100);
                return;
            }
            
            try {
                // Prepare the authentication message for Decap CMS
                const authData = {
                    access_token: token,
                    token_type: 'bearer',
                    provider: provider,
                    scope: 'repo,user'
                };
                
                // Format exactly as Decap CMS expects
                const message = 'authorization:github:success:' + JSON.stringify(authData);
                window.opener.postMessage(message, '*');
                
                // Close the window after sending the message
                setTimeout(() => {
                    window.close();
                }, 500);
            } catch (e) {
                console.error('Error sending auth data:', e);
                document.body.innerHTML = '<p>Error: ' + e.message + '</p>';
            }
        }
        
        // Start the process when the page loads
        if (window.opener && !window.opener.closed) {
            sendAuthData();
        } else {
            // Poll for opener availability
            const checkOpener = setInterval(() => {
                if (window.opener && !window.opener.closed) {
                    clearInterval(checkOpener);
                    sendAuthData();
                }
            }, 100);
            
            // Give up after 5 seconds
            setTimeout(() => {
                clearInterval(checkOpener);
                document.body.innerHTML = '<p>Could not connect to opener window. Please try again.</p>';
            }, 5000);
        }
    </script>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' },
        status: 200
    });
}