# The Sense of Nonsense

An investigative publication by **Lars J. Frank**.

> Stories and analysis from within the nonsense.

Public documents. Public interest. An engineer writing within the water-energy-food nexus, primarily about the distance between what the public is told about carbon accounting and what is actually happening in the ledgers, filings, and regulatory systems that define it.

Built with [Hugo](https://gohugo.io/) and deployed on [Cloudflare Pages](https://pages.cloudflare.com/).

---

## How to run locally

### Prerequisites

Install Hugo (extended edition, v0.145+):

- **macOS:** `brew install hugo`
- **Linux:** Download from [Hugo releases](https://github.com/gohugoio/hugo/releases)
- **Windows:** `winget install Hugo.Hugo.Extended`

Verify:

```sh
hugo version
```

### Serve the site

```sh
hugo server -D
```

Opens at `http://localhost:1313`. The `-D` flag shows draft content.

### Build for production

```sh
hugo
```

Output goes to `public/`. This is the directory Cloudflare Pages deploys.

---

## Content authoring

### Create a new essay

```sh
hugo new content essays/your-essay-title.md
```

Then edit `content/essays/your-essay-title.md`. Set `draft: false` when ready to publish.

### Create a new series

1. Create a series landing page:

```sh
mkdir -p content/series/your-series-name
hugo new content series/your-series-name/_index.md
```

Edit the `_index.md` to set `type: "series-landing"` and add a description.

2. Create parts as regular pages within the series directory:

```sh
hugo new content series/your-series-name/part-1-title.md
```

Set `series: "Your Series Name"` and `part: 1` in the front matter.

### Front matter fields

```yaml
---
title: "Article Title"
date: 2026-07-09
draft: true                     # set false to publish
summary: "Short summary shown on listing pages"
series: "The TIER Files"        # optional: associate with a series
part: 1                         # optional: ordering within a series
featured: true                  # optional: show on home page
topics: ["alberta", "carbon"]   # optional: taxonomy tags
aliases: ["/old-url/"]          # optional: redirects
---
```

## Deploy to Cloudflare Pages

### 1. Push to GitHub

```sh
git init
git add .
git commit -m "Initial site"
gh repo create thesenseofnonsense --public --source=. --remote=origin --push
```

(Or use `git remote add origin <url>` if you create the repo manually.)

### 2. Connect to Cloudflare Pages

1. Go to **Workers & Pages** in the Cloudflare dashboard.
2. Click **Create application** → **Pages**.
3. Connect your GitHub account and select `thesenseofnonsense`.
4. Set these build options:

   | Setting | Value |
   |---------|-------|
   | Production branch | `main` |
   | Build command | `hugo` |
   | Build output directory | `public` |

5. (Recommended) Add an environment variable:

   | Variable | Value |
   |----------|-------|
   | `HUGO_VERSION` | `0.145.0` |

6. Click **Save and Deploy**.

### 3. Add a custom domain

1. Go to your Pages project → **Custom domains** → **Set up a custom domain**.
2. Enter `thesenseofnonsense.com`.
3. Cloudflare will auto-provision the DNS record if the domain is on your account.

The site builds from `main`. Content with `draft: true` is skipped in production builds.

---

## License

Content &copy; Lars J. Frank. All rights reserved.

Source code (theme, layout, configuration) is MIT licensed.