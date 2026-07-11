/**
 * Decap CMS auth start.
 *
 * Preferred: GitHub OAuth App via GITHUB_CLIENT_ID (+ secret on /api/callback).
 * Fallback: GITHUB_TOKEN with Decap's postMessage handshake (single-author bridge).
 */
function renderPatHandshake(token) {
  const payload = JSON.stringify({ token, provider: "github" });
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Decap CMS Authentication</title>
  <style>
    body { font-family: system-ui, sans-serif; text-align: center; padding: 2rem; color: #222; }
  </style>
</head>
<body>
  <p>Authentication complete. You can close this window.</p>
  <script>
    (function () {
      function receiveMessage(message) {
        window.opener.postMessage(
          "authorization:github:success:${payload}",
          message.origin
        );
        window.removeEventListener("message", receiveMessage, false);
      }
      window.addEventListener("message", receiveMessage, false);
      if (window.opener) {
        window.opener.postMessage("authorizing:github", "*");
      } else {
        document.body.innerHTML = "<p>Open this page from the Decap CMS login popup.</p>";
      }
    })();
  </script>
</body>
</html>`;
}

export async function onRequest({ request, env }) {
  const clientId = String(env.GITHUB_CLIENT_ID || "").trim();
  const pat = String(env.GITHUB_TOKEN || "").trim();

  if (clientId) {
    const url = new URL(request.url);
    const redirectUri = `${url.origin}/api/callback`;
    const authorize = new URL("https://github.com/login/oauth/authorize");
    authorize.searchParams.set("client_id", clientId);
    authorize.searchParams.set("redirect_uri", redirectUri);
    authorize.searchParams.set("scope", "repo user");
    authorize.searchParams.set("state", crypto.randomUUID());
    return Response.redirect(authorize.href, 302);
  }

  if (pat) {
    return new Response(renderPatHandshake(pat), {
      status: 200,
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-store",
      },
    });
  }

  return new Response(
    "Decap auth is not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET (OAuth App), or GITHUB_TOKEN as a temporary bridge.",
    { status: 500, headers: { "Content-Type": "text/plain; charset=utf-8" } },
  );
}
