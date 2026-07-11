export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined') {
        return new Response('Missing GITHUB_TOKEN env var', { status: 500 });
    }

    // Simple approach: set token in localStorage and redirect to admin
    const html = `<!DOCTYPE html>
<html>
<body>
<p>Logging in...</p>
<script>
  // Store user data in localStorage as Decap CMS expects
  const userData = {
    token: '${token}',
    provider: 'github'
  };
  localStorage.setItem('gitcms-user', JSON.stringify(userData));
  
  // Redirect to admin panel
  window.location.href = '/admin/';
</script>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
}