/**
 * Decap CMS auth start.
 *
 * Preferred: GitHub OAuth App via GITHUB_CLIENT_ID (+ secret on /api/callback).
 * Fallback: GITHUB_TOKEN with Decap's postMessage handshake (single-author bridge).
 */
function renderPatHandshake(token) {
  // Embed as a JS object literal. Do not splice JSON into a "..." string
  // (quotes in the token JSON would break the script and silent-fail login).
  const authDataJs = JSON.stringify({ token, provider: "github" });
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Decap CMS Authentication</title>
  <style>
    body { font-family: system-ui, sans-serif; text-align: center; padding: 2rem; color: #222; }
    #status { color: #555; }
  </style>
</head>
<body>
  <p id="status">Completing authentication…</p>
  <script>
    (function () {
      var authData = ${authDataJs};
      var statusEl = document.getElementById("status");

      function receiveMessage(message) {
        if (!window.opener) return;
        window.opener.postMessage(
          "authorization:github:success:" + JSON.stringify(authData),
          message.origin
        );
        window.removeEventListener("message", receiveMessage, false);
        statusEl.textContent = "Authentication complete. You can close this window.";
        setTimeout(function () { try { window.close(); } catch (e) {} }, 500);
      }

      window.addEventListener("message", receiveMessage, false);

      if (!window.opener) {
        statusEl.textContent = "Open this page from the Decap CMS login popup.";
        return;
      }

      // Decap handshake: popup announces, parent echoes, popup sends token.
      window.opener.postMessage("authorizing:github", "*");
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
