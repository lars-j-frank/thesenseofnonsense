export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined') {
        return new Response('Missing GITHUB_TOKEN env var', { status: 500 });
    }

    // The implicit auth flow: set token in localStorage and redirect to admin
    const html = `<!DOCTYPE html>
<html>
<body>
<p>Logging in...</p>
<script>
  // Decap CMS stores user data in localStorage under this key
  var user = {
    token: '${token}',
    provider: 'github',
    backendName: 'github',
    name: 'lars-j-frank',
    login: 'lars-j-frank',
    email: 'lars-j-frank@users.noreply.github.com',
    avatar_url: 'https://github.com/lars-j-frank.png'
  };
  localStorage.setItem('decap-cms-user', JSON.stringify(user));
  window.location.href = '/admin/';
</script>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
}