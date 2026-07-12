/**
 * Decap CMS auth start — GitHub OAuth App only.
 *
 * Never embed a personal access token in HTML. A PAT fallback would be
 * world-readable at /api/auth and grants repo write access to anyone.
 *
 * Cloudflare Pages secrets required:
 *   GITHUB_CLIENT_ID
 *   GITHUB_CLIENT_SECRET  (used by /api/callback)
 */
export async function onRequest({ request, env }) {
  const clientId = String(env.GITHUB_CLIENT_ID || "").trim();

  if (!clientId) {
    return new Response(
      [
        "Decap auth is not configured.",
        "Create a GitHub OAuth App for this site and set GITHUB_CLIENT_ID",
        "and GITHUB_CLIENT_SECRET on Cloudflare Pages.",
        "Do not use a personal access token bridge.",
      ].join(" "),
      { status: 503, headers: { "Content-Type": "text/plain; charset=utf-8" } },
    );
  }

  const url = new URL(request.url);
  const redirectUri = `${url.origin}/api/callback`;
  const authorize = new URL("https://github.com/login/oauth/authorize");
  authorize.searchParams.set("client_id", clientId);
  authorize.searchParams.set("redirect_uri", redirectUri);
  authorize.searchParams.set("scope", "repo");
  authorize.searchParams.set("state", crypto.randomUUID());
  return Response.redirect(authorize.href, 302);
}
