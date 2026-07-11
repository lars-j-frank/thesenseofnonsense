/**
 * Decap CMS GitHub OAuth - callback
 * Exchanges ?code= for a token, then completes Decap's postMessage handshake:
 *   1) popup -> opener: "authorizing:github"
 *   2) opener replies with its origin
 *   3) popup -> opener: "authorization:github:success:{ token, provider }"
 */
function renderBody(status, content) {
  const payload = JSON.stringify(content);
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
  <p>${status === "success" ? "Authentication complete. You can close this window." : "Authentication failed."}</p>
  <script>
    (function () {
      function receiveMessage(message) {
        window.opener.postMessage(
          "authorization:github:${status}:${payload}",
          message.origin
        );
        window.removeEventListener("message", receiveMessage, false);
      }
      window.addEventListener("message", receiveMessage, false);
      window.opener.postMessage("authorizing:github", "*");
    })();
  </script>
</body>
</html>`;
}

export async function onRequest({ request, env }) {
  const clientId = String(env.GITHUB_CLIENT_ID || "").trim();
  const clientSecret = String(env.GITHUB_CLIENT_SECRET || "").trim();

  if (!clientId || !clientSecret) {
    return new Response(
      renderBody("error", {
        error: "missing_oauth_secrets",
        error_description:
          "Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET on Cloudflare Pages.",
      }),
      { status: 500, headers: { "Content-Type": "text/html; charset=utf-8" } },
    );
  }

  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const oauthError = url.searchParams.get("error");

  if (oauthError) {
    return new Response(
      renderBody("error", {
        error: oauthError,
        error_description: url.searchParams.get("error_description") || "",
      }),
      { status: 400, headers: { "Content-Type": "text/html; charset=utf-8" } },
    );
  }

  if (!code) {
    return new Response(
      renderBody("error", {
        error: "missing_code",
        error_description: "GitHub did not return an authorization code.",
      }),
      { status: 400, headers: { "Content-Type": "text/html; charset=utf-8" } },
    );
  }

  try {
    const tokenRes = await fetch("https://github.com/login/oauth/access_token", {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        "User-Agent": "thesenseofnonsense-decap-oauth",
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code,
        redirect_uri: `${url.origin}/api/callback`,
      }),
    });

    const result = await tokenRes.json();
    if (result.error || !result.access_token) {
      return new Response(renderBody("error", result), {
        status: 401,
        headers: { "Content-Type": "text/html; charset=utf-8" },
      });
    }

    return new Response(
      renderBody("success", {
        token: result.access_token,
        provider: "github",
      }),
      { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } },
    );
  } catch (err) {
    return new Response(
      renderBody("error", {
        error: "token_exchange_failed",
        error_description: String(err && err.message ? err.message : err),
      }),
      { status: 500, headers: { "Content-Type": "text/html; charset=utf-8" } },
    );
  }
}
