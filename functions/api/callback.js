export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    const html = `<!DOCTYPE html>
<html>
<body>
<script>
  const payload = 'authorization:github:success:' + JSON.stringify({
    token: '${token}',
    provider: 'github',
    backendName: 'github'
  });
  window.opener.postMessage(payload, '*');
  window.close();
</script>
<p>Authenticated. Closing...</p>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
}