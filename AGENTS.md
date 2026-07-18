# The Sense of Nonsense — Site Context

## Overview

Investigative publication by **Lars J. Frank** (pseudonym). Focused on carbon accounting, public finance, and the gap between official narratives and audited statements. Built with Hugo, deployed on Cloudflare Pages.

- **Domain:** thesenseofnonsense.com
- **Repo:** github.com/lars-j-frank/thesenseofnonsense (public)
- **Author identity:** Lars J. Frank <lars.j.frank@protonmail.com>
- **Tagline:** "Stories and analysis from within the nonsense"
- **Tone:** restrained, literate, skeptical, technical, not performative — "reads annual reports for sport"
- **Copy ban:** Do not use "The story is in the ledger" or slogan variants of it (reads as AI tagline). Stick to the site tagline or plain documentary phrasing.

## Tech Stack

| Layer | Choice |
|-------|--------|
| Static site generator | Hugo v0.145.0 (extended) |
| Theme | Custom in-repo (`themes/sense/`) — no third-party themes or submodules |
| CSS | Custom editorial theme — light only (no `prefers-color-scheme` dark mode) |
| Fonts | Source Serif 4 (body/headlines) + Libre Franklin (UI/nav) via Google Fonts |
| JS | Minimal — mobile nav toggle only |
| Hosting | Cloudflare Pages (Git-based integration) |
| Build command | `hugo` |
| Output directory | `public` |
| Production branch | `main` |
| Env var | `HUGO_VERSION=0.145.0` |
| Taxonomies | `topics` only (`series` is a plain front-matter field, not a Hugo taxonomy — avoids clashing with `/series/…` section URLs) |

## Content Architecture

```
content/
├── _index.md              # Homepage (uses site params for content)
├── about.md               # About Lars J. Frank
├── archive.md             # Reverse-chronological listing (auto-generated)
├── essays/_index.md       # Standalone essays section
├── series/
│   ├── _index.md          # Series listing
│   └── the-tier-files/
│       ├── _index.md      # Series landing page (type: series-landing)
│       └── part-N-…/index.md   # page bundles
└── topics/_index.md       # Taxonomy listing
```

### Front matter fields

```yaml
title: "Article Title"
date: 2026-07-09
draft: true                    # set false to publish
summary: "One-line summary"    # shown on listing pages
series: "The TIER Files"       # associate with a series
part: 1                        # ordering within series
featured: true                 # show on homepage featured block
topics: ["alberta", "carbon"]  # taxonomy tags
url: "/custom/path/"           # only when explicit URL needed
```

### Content types

- **essays** — standalone long-form articles under `/essays/:slug/`
- **series** — grouped investigations with parent landing page under `/series/:slug/`
- **series parts** — individual articles with `url` front matter to nest under series path
- **about** — single page
- **archive** — auto-generated reverse-chronological listing

## Custom Theme (`themes/sense/`)

```
layouts/
├── _default/
│   ├── baseof.html       # HTML shell with header, nav, footer
│   ├── single.html       # Article page with series nav + prev/next
│   ├── list.html         # Section listing (essays, series index)
│   ├── archive.html      # Archive page
│   ├── about.html        # About page
│   ├── series-landing.html  # Series landing with ordered parts list
│   ├── topics.html       # Topic cloud page
│   └── term.html         # Individual topic page
└── index.html            # Homepage: featured articles, series, recent list
```

### Design properties

- Narrow reading width (~680px for articles)
- Light magazine palette (white canvas; Glossy Red `#DE0000` / Deep Bright Red `#B50000` accents; Rich Grey `#3C3D3C`, Manhattan `#525252`, Titanium `#8B8783`) — light theme only; no auto dark mode
- Serif display/body (Source Serif 4), sans UI (Libre Franklin)
- Feature images: `cover.png` in page bundles; charts via `scripts/regen-tier-charts.py` and `scripts/gen-draft-charts.py`
- CSS cache-bust via `sense.css?v=N` in `baseof.html`; chart images via `?v=N` on markdown refs
- Hugo templates: do not chain `else if` after `with` (Cloudflare Pages / Hugo parse failure)

## Writing workflow (Word DOCX — same idea as Whitepaper studio)

Prose is edited in Word (including phone via Drive). Markdown in `content/` remains the Hugo source of truth. Front matter never enters the DOCX.

**Drop zone:** `%USERPROFILE%\Documents\writing\larsjf\` (PDF/DOCX for Drive sync). Hash stamps live in `.sync\`.

| Script | Purpose |
|--------|---------|
| `scripts/export-all-writing.ps1` | Export every article body → `writing\larsjf\<stem>.docx` |
| `scripts/export-docx.ps1 -MdPath …` | Export one article |
| `scripts/check-writing-edits.ps1` | **Always run first** — import Word edits if DOCX hash ≠ last export |
| `scripts/import-docx-if-newer.ps1 -MdPath …` | Import one article |

**Agent rule:** Before editing any article under `content/`, run `.\scripts\check-writing-edits.ps1`. If it imports changes (exit code 2), treat the updated markdown as authoritative and do not overwrite those edits. After substantive markdown edits, re-run `.\scripts\export-all-writing.ps1` (or `export-docx.ps1` for the touched piece).

Edit detection is SHA-256 based (not timestamps), matching the Whitepaper `docx-sync.json` pattern.

## Cloudflare Pages Setup

1. Git integration → `lars-j-frank/thesenseofnonsense`
2. Build: `hugo`, output: `public`
3. Production branch: `main`
4. Env: `HUGO_VERSION=0.145.0`
5. Custom domain: thesenseofnonsense.com

No CMS and no Pages Functions. In the Cloudflare Pages project, delete any leftover secrets that existed for the old CMS login. On GitHub, delete any OAuth App that was created for `/admin` if it still exists.

Deploys on push to `main`. Drafts (`draft: true`) are skipped in production.

## Git Workflow

```powershell
hugo server -D
hugo
git add <paths>   # never git add -A
git commit -m "description"
git push origin main
```

Commit author for this repo: Lars J. Frank / lars.j.frank@protonmail.com. Push as the `lars-j-frank` GitHub account only.

## Content Authoring

1. Run `.\scripts\check-writing-edits.ps1`
2. Edit `content/.../index.md` (or the matching DOCX, then check-writing-edits)
3. `hugo server -D` to preview
4. `.\scripts\export-docx.ps1` / `export-all-writing.ps1` after markdown changes
5. Commit and push when ready to publish (`draft: false`)

```powershell
hugo new content essays/your-essay-title/index.md
hugo new content series/the-tier-files/part-8-title/index.md
```

Series parts must set `series: "The TIER Files"` (exact landing title) and `part: N`. Prefer page bundles.

## House copy rules

- No em dashes; Canadian spelling (per cent); no define-by-negation tropes; no AI tell phrases
- Connection ≠ causation; every number from a named public document
- Omit leading “The” from short titles, labels, and short sentences when meaning remains clear. Prefer direct labels (Overview, Findings, Float) over format-explaining labels (The series in one sentence). Keep “The” in proper names such as The TIER Files. Show content; do not describe its format.

## Future Work

- [ ] Part 8 ahead of the next TIER statutory review (deadline moved to Dec 2030 by O.C. 369/2025)
- [ ] More topics as content grows
- [ ] Optional RSS enhancements
