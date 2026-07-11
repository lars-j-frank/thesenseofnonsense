# Decap CMS — content workflow

CMS: https://thesenseofnonsense.com/admin/

Primary way to write and edit site content (mobile or desktop). Prefer Decap over hand-editing Markdown in git unless you are changing theme/code.

## What you can edit

| Collection | Use for |
|------------|---------|
| **The TIER Files** | Series articles (page bundles with images) |
| **Essays** | Standalone essays |
| **Pages** | About, series landing copy, section intros |

Homepage tagline/description still live in `hugo.toml` (code), not Decap.

## Mobile / everyday workflow

1. Open `/admin/` and **Login with GitHub** (as `lars-j-frank`).
2. Open or create an entry.
3. Write in the editor. Decap **autosaves drafts** under the editorial workflow (GitHub branch/PR).
4. Set **Draft** to off when the piece should be buildable by Hugo.
5. Click **Publish** — Decap merges to `main`; Cloudflare Pages rebuilds the site.

Until you Publish, draft work is not on the live site.

## Images

TIER Files and Essays use Hugo **page bundles** (`content/.../your-slug/index.md` plus images in the same folder).

- Upload images from the Decap media UI while editing that article.
- In Markdown, use `![alt](filename.png)` or existing Hugo shortcodes such as `{{</* figure src="filename.png" ... */>}}`.

Global fallback media folder: `static/images` → `/images/...` on the site.

## New TIER Files part

1. Collection **The TIER Files** → New Article.
2. Set **URL slug** first (e.g. `part-2-the-next-chapter`) — that becomes the folder name.
3. Set **Series** to exactly `The TIER Files` (must match the series landing title).
4. Set **Part number**, body, topics, images.
5. Leave Draft on while writing; Publish when ready.

## Auth notes

Production currently uses a `GITHUB_TOKEN` bridge for Decap login. Prefer upgrading to a GitHub OAuth App (`GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET`) when convenient — see earlier setup notes in git history / Cloudflare secrets. Rotate the PAT after OAuth is live.

## Repo layout (for reference)

```
static/admin/config.yml   # Decap collections (source of truth for CMS fields)
static/admin/index.html   # Decap shell
functions/api/auth.js     # Login start
functions/api/callback.js # OAuth callback
content/                  # All CMS-managed Markdown
```
