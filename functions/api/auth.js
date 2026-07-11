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
  // Function to send the token to the opener (the main Decap CMS window)
  const sendToken = () => {
    if (window.opener && !window.opener.closed) {
      const message = 'authorization:github:success:' + JSON.stringify({
        access_token: '${token}',
        token_type: 'bearer'
      });
      window.opener.postMessage(message, '*');
      // Send a few times to increase chance of being received
      setTimeout(sendToken, 500);
      setTimeout(sendToken, 1000);
      setTimeout(sendToken, 1500);
    } else {
      // Opener is closed or not available, we can close this window
      window.close();
    }
  };

  // Start sending after a short delay to allow the opener to set up its listener
  setTimeout(sendToken, 1000);
</script>
</body>
</html>`;

    return new Response(html, {
        headers: { 'Content-Type': 'text/html;charset=UTF-8' }
    });
}