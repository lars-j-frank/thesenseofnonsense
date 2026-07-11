export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    const html = `<!DOCTYPE html>
<html>
<body>
<script>
  var match = window.location.search.match(/access_token=([^&]+)/);
  var token = match ? match[1] : '${token}';
  var user = {
    token: token,
    provider: 'github',
    backendName: 'github',
    name: 'lars-j-frank',
    login: 'lars-j-frank'
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