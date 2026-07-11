# Decap CMS setup (Cloudflare Pages + GitHub)

CMS UI: https://thesenseofnonsense.com/admin/

- Cloudflare Pages project: `thesenseofnonsense`
- GitHub repo: `lars-j-frank/thesenseofnonsense`

## Current auth mode

`/api/auth` supports two modes:

1. **OAuth App (preferred):** set `GITHUB_CLIENT_ID` + `GITHUB_CLIENT_SECRET` on Pages
2. **PAT bridge (temporary):** set `GITHUB_TOKEN` on Pages; Decap login uses the correct `postMessage` handshake

Production currently uses the PAT bridge so login works without a browser OAuth App session. Upgrade to an OAuth App when you can (keeps the token out of HTML).

## Upgrade to a GitHub OAuth App

1. Sign in as **lars-j-frank** (or any account; Decap users still authorize as themselves).
2. https://github.com/settings/developers → **OAuth Apps** → **New OAuth App**
3. Fields:
   - Application name: `The Sense of Nonsense CMS`
   - Homepage URL: `https://thesenseofnonsense.com`
   - Authorization callback URL: `https://thesenseofnonsense.com/api/callback`
4. Create the app, generate a client secret, then set Pages secrets:

```powershell
npx wrangler pages secret put GITHUB_CLIENT_ID --project-name thesenseofnonsense
npx wrangler pages secret put GITHUB_CLIENT_SECRET --project-name thesenseofnonsense
```

After OAuth secrets are present, `/api/auth` redirects to GitHub authorize instead of the PAT bridge. You can remove `GITHUB_TOKEN` once OAuth is verified.

## Login

1. Open https://thesenseofnonsense.com/admin/
2. Click **Login with GitHub**
3. For OAuth mode, approve as `lars-j-frank`
4. Edit TIER Files / Essays. `editorial_workflow` publishes via pull requests.

## Files

| Path | Role |
|------|------|
| `static/admin/index.html` | Decap shell |
| `static/admin/config.yml` | Backend + collections |
| `functions/api/auth.js` | OAuth start or PAT handshake |
| `functions/api/callback.js` | OAuth code exchange + handshake |
