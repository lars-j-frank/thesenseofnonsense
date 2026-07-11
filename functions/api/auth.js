export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    // Return a page that posts the token back to Decap CMS
    const html = `<!DOCTYPE html>
<html>
<body>
<script>
  // Small delay to ensure the opener is ready
  setTimeout(() => {
    const payload = 'authorization:github:success:' + JSON.stringify({
      token: '${token}',
      provider: 'github',
      backendName: 'github'
    });
    window.opener.postMessage(payload, '*');
    window.close();
  }, 500);
</script>
<p>Authenticating... this window will close automatically.</p>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
}