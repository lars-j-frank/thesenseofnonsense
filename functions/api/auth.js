export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined' || token === '') {
        return new Response('Missing or empty GITHUB_TOKEN', { status: 500 });
    }

    // Clean the token
    const cleanToken = token.trim();

    // Return HTML that stores token in localStorage and redirects to admin
    return new Response(`<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Logging in...</title>
</head>
<body>
    <p>Logging in...</p>
    <script>
        // Store user data in localStorage for Decap CMS
        const userData = {
            token: '${cleanToken}',
            provider: 'github'
        };
        localStorage.setItem('gitcms-user', JSON.stringify(userData));
        localStorage.setItem('decap-cms-user', JSON.stringify(userData));
        localStorage.setItem('netlify-cms-user', JSON.stringify(userData));
        
        // Redirect to the admin panel
        window.location.href = '/admin/';
    </script>
</body>
</html>`, {
        headers: {
            'Content-Type': 'text/html;charset=UTF-8'
        }
    });
}