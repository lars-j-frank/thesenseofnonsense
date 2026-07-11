export async function onRequest(context) {
    const { env } = context;
    const token = env.GITHUB_TOKEN;

    if (!token || token === 'undefined') {
        return new Response('Missing GITHUB_TOKEN env var', { status: 500 });
    }

    const html = `<!DOCTYPE html>
<html>
<body>
<p>Authenticating...</p>
<script>
  // Decap CMS opens this in a popup and waits for postMessage
  // The format must be exactly: authorization:<provider>:<status>:<data JSON>
  const sendToken = () => {
    const data = JSON.stringify({ token: '${token}', provider: 'github' });
    const payload = 'authorization:github:success:' + data;
    window.opener.postMessage(payload, '*');
  };

  // Try multiple times in case Decap CMS listener isn't ready
  setTimeout(sendToken, 800);
  setTimeout(sendToken, 1500);
  setTimeout(sendToken, 2500);
  setTimeout(() => window.close(), 3000);
</script>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
}