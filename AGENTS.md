# The Sense of Nonsense — Site Context

## Overview

Investigative publication by **Lars J. Frank** (pseudonym). Focused on carbon accounting, public finance, and the gap between official narratives and audited statements. Built with Hugo, deployed on Cloudflare Pages.

- **Domain:** thesenseofnonsense.com
- **Repo:** github.com/lars-j-frank/thesenseofnonsense (public)
- **Author identity:** Lars J. Frank <lars.j.frank@protonmail.com>
- **Tagline:** "The story is in the ledger."
- **Tone:** restrained, literate, skeptical, technical, not performative — "reads annual reports for sport"

## Tech Stack

| Layer | Choice |
|-------|--------|
| Static site generator | Hugo v0.145.0 (extended) |
| Theme | Custom in-repo (`themes/sense/`) — no third-party themes or submodules |
| CSS | Custom editorial theme, light/dark mode via `prefers-color-scheme` |
| Fonts | Lora (serif, body) + Inter (sans-serif, headings/nav) via Google Fonts |
| JS | Minimal — mobile nav toggle only |
| Hosting | Cloudflare Pages (Git-based integration) |
| Build command | `hugo` |
| Output directory | `public` |
| Production branch | `main` |
| Env var | `HUGO_VERSION=0.145.0` |

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
│       └── part-1-the-billion-dollar-detour.md
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
- **series parts** — individual articles with `url` front matter to nest under series path, e.g. `/series/the-tier-files/part-1-the-billion-dollar-detour/`
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

### Series navigation

Series articles use `series` + `part` front matter. The single.html template automatically:
- Shows a "Part of [Series]" block with ordered parts list
- Highlights the current article
- Provides prev/next within section

### Design properties

- Narrow reading width (680px for articles)
- Neutral base palette, one muted accent (#8B4513 saddle brown)
- Light mode: off-white background (#faf9f7)
- Dark mode: dark background (#141413), auto-switches via system preference
- Serif body (Lora), sans-serif headings (Inter)
- No cards, no gradients, no startup aesthetic — editorial, list-based layouts

## Current Content

- **Homepage** — tagline, intro, featured article block, series block, recent list
- **About** — pen name explanation, public records ethos
- **The TIER Files series** — landing page with description
- **Part 1: The Billion-Dollar Detour** — seeded with placeholder body (awaiting full draft)

## Cloudflare Pages Setup

Set up via Git integration at dash.cloudflare.com:
1. Connected to `lars-j-frank/thesenseofnonsense`
2. Build command: `hugo`, output: `public`
3. Production branch: `main`
4. Env var: `HUGO_VERSION=0.145.0`
5. Custom domain: thesenseofnonsense.com

Deploys automatically on push to `main`. Draft content (`draft: true`) is skipped in production.

## Git Workflow

```bash
# Preview locally
hugo server -D

# Build for production
hugo

# Deploy
git add -A
git commit -m "description"
git push origin main
```

Push access via `lars-j-frank` GitHub account. PAT stored as `LARS_GITHUB_TOKEN` env var in the WSL Hermes profile.

## Content Authoring Guide

**Primary editor:** Decap CMS at https://thesenseofnonsense.com/admin/ (see `DECAP_SETUP.md`). Use it for articles, essays, About, and series landing copy — including mobile. Autosave + Publish go through GitHub; Cloudflare rebuilds from `main`.

### CLI fallback (theme/code or offline)

```bash
hugo new content essays/your-essay-title/index.md
hugo new content series/the-tier-files/part-2-title/index.md
hugo server -D
```

Series parts must set `series: "The TIER Files"` (exact landing title) and `part: N`. Prefer page bundles (`slug/index.md` + images in the same folder).

### Publish workflow (Decap)

1. Edit in `/admin/`
2. Drafts autosave via editorial workflow
3. Set Draft off when ready for Hugo to build the page
4. Publish → merge to `main` → Cloudflare deploy

## Editing Environment

Windows path: `[operator-local-clone]`. Push as `lars-j-frank` (not `lars-j-frank`) to preserve the anonymous GitHub identity.

## Future Work

- [ ] Write additional TIER Files parts (via Decap)
- [ ] Write standalone essays (via Decap)
- [ ] Add more topics as content grows
- [ ] Upgrade Decap auth from PAT bridge to GitHub OAuth App
- [ ] Consider RSS feed enhancements if needed