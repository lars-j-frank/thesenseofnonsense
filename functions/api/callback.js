/**
 * Decap CMS GitHub OAuth - callback
 * Exchanges ?code= for a token, then completes Decap's postMessage handshake.
 */
function renderBody(status, content) {
  const authDataJs = JSON.stringify(content);
  const ok = status === "success";
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
  <p id="status">${ok ? "Completing authentication…" : "Authentication failed."}</p>
  <script>
    (function () {
      var status = ${JSON.stringify(status)};
      var authData = ${authDataJs};
      var statusEl = document.getElementById("status");

      function receiveMessage(message) {
        if (!window.opener) return;
        window.opener.postMessage(
          "authorization:github:" + status + ":" + JSON.stringify(authData),
          message.origin
        );
        window.removeEventListener("message", receiveMessage, false);
        if (status === "success") {
          statusEl.textContent = "Authentication complete. You can close this window.";
          setTimeout(function () { try { window.close(); } catch (e) {} }, 500);
        }
      }

      window.addEventListener("message", receiveMessage, false);
      if (window.opener) {
        window.opener.postMessage("authorizing:github", "*");
      } else {
        statusEl.textContent = "Open this page from the Decap CMS login popup.";
      }
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
