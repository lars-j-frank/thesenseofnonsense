# Lars J. Frank — LinkedIn kit

**Prepared:** 17 July 2026  
**Publication:** [The Sense of Nonsense](https://thesenseofnonsense.com)  
**Contact:** [lars.j.frank@protonmail.com](mailto:lars.j.frank@protonmail.com)

## Mark, not a face

Lars is a disclosed pen name. No synthetic headshot. No portrait of the real person. Profile photo is the LF monogram: Rich Grey field, Glossy Red spine, white initials. Same system as `static/logo.svg`.

| Asset | Role |
|---|---|
| **LF avatar** | Personal LinkedIn profile photo |
| **SN mark** | Site / optional Company page only |
| **Banner** | Name, publication, site tagline |

## What to upload

| LinkedIn slot | File | Spec |
|---|---|---|
| Profile photo | `assets/avatar-lf-800.png` | 800×800 |
| Background / banner | `assets/banner-primary-1584x396.png` | 1584×396 |
| Alt banner | `assets/banner-ledger-1584x396.png` | darker, tagline-forward |
| Brand board | `assets/brand-board.png` | reference only |

```powershell
py -3 brand/linkedin/scripts/render-linkedin-assets.py
```

Paste-ready fields: [`PROFILE_COPY.md`](PROFILE_COPY.md).

## Brand tokens

| Token | Hex |
|---|---|
| Glossy Red | `#DE0000` |
| Deep Bright Red | `#B50000` |
| Rich Grey | `#3C3D3C` |
| Manhattan | `#525252` |
| Titanium | `#8B8783` |
| Canvas | `#FFFFFF` |

**Type:** Source Serif 4 · Libre Franklin  
**Site tagline:** Stories and analysis from within the nonsense

Do not invent slogans. Use the site line above, or leave the banner to name + publication only.

## Upload checklist

1. Profile as **Lars J. Frank**.
2. LF avatar + primary banner.
3. Headline + About from `PROFILE_COPY.md`.
4. Featured: series landing, Part 1, press.
5. Contact: ProtonMail + thesenseofnonsense.com.
6. Optional Company page with SN mark.
7. Disclose the pen name to editors (`docs/PRESS_KIT.md`).

## Do not

- AI faces or stock portraits.
- SN mark as the personal avatar.
- Slogan variants of “the story is in the…” or other campaign-style taglines.
- Overclaim beyond the press kit.
