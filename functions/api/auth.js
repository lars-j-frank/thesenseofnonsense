export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined' || token.trim() === '') {
        return new Response('Missing or empty GITHUB_TOKEN environment variable', { 
            status: 500,
            headers: { 'Content-Type': 'text/plain' }
        });
    }

    // Clean the token - remove any whitespace that might have been added
    const cleanToken = token.trim();

    const html = `<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Authenticating...</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 2rem; }
    </style>
</head>
<body>
    <p>Authenticating with GitHub...</p>
    <p>This window will close automatically.</p>
    
    <script>
        // Wait for the opener to be available and ready to receive messages
        function sendAuthMessage() {
            if (!window.opener || window.opener.closed) {
                // Opener not available yet, try again in a moment
                setTimeout(sendAuthMessage, 100);
                return;
            }
            
            try {
                const message = {
                    token: '${cleanToken}',
                    provider: 'github'
                };
                
                // Send the exact format Decap CMS expects
                const payload = 'authorization:github:success:' + JSON.stringify(message);
                window.opener.postMessage(payload, '*');
                
                // Close window after a brief delay to ensure message is received
                setTimeout(() => {
                    window.close();
                }, 500);
            } catch (e) {
                console.error('Error sending auth message:', e);
                document.body.innerHTML = '<p>Error: ' + e.message + '</p>';
            }
        }
        
        // Start the process when the page loads
        if (window.opener && !window.opener.closed) {
            sendAuthMessage();
        } else {
            // Poll for opener availability
            const checkOpener = setInterval(() => {
                if (window.opener && !window.opener.closed) {
                    clearInterval(checkOpener);
                    sendAuthMessage();
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