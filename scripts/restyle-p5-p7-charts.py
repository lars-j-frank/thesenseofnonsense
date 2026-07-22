"""Restyle Part 5-7 diagrams and covers to the site red/grey editorial palette.

Brings p5-claim-layers, p6-edge-types, p6-pipeline, p7-two-eras, and the
Part 6 / Part 7 covers in line with the charts in Parts 1-4 and Ghost Lives
(regen-tier-charts.py style).
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "content" / "series" / "the-tier-files"
P5 = SERIES / "part-5-paid-in-alberta-claimed-everywhere"
P6 = SERIES / "part-6-the-small-world"
P7 = SERIES / "part-7-the-companies-the-board-pays-itself"

BG = "#FFFFFF"
WASH = "#F3F3F2"
INK = "#3C3D3C"
MUTED = "#8B8783"
MUTED_LIGHT = "#C5C3C0"
HIGHLIGHT = "#DE0000"
SECONDARY = "#525252"
GRID = "#D6D4D1"

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
})


def style_ax(ax, title: str):
    ax.set_facecolor(BG)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK, labelsize=10)
    ax.set_title(title, loc="left", fontsize=13, fontweight="bold", color=INK, pad=10)


def save(fig, path: Path, source: str):
    fig.patch.set_facecolor(BG)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.012, source, fontsize=8, color=MUTED)
    fig.savefig(path, dpi=180, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def make_cover(chart_path: Path, out: Path, part: int, title: str, subtitle: str = ""):
    chart = Image.open(chart_path).convert("RGB")
    W, H = 1600, 1000
    cover = Image.new("RGB", (W, H), WASH)
    pad = 56
    band_h = 200
    area_w, area_h = W - 2 * pad, H - band_h - pad - 24
    sw, sh = chart.size
    scale = min(area_w / sw, area_h / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = chart.resize((nw, nh), Image.Resampling.LANCZOS)
    panel = Image.new("RGB", (area_w, area_h), BG)
    panel.paste(resized, ((area_w - nw) // 2, (area_h - nh) // 2))
    cover.paste(panel, (pad, pad))
    d = ImageDraw.Draw(cover)
    d.rectangle([0, 0, 8, H], fill=HIGHLIGHT)
    d.rectangle([0, H - band_h, W, H], fill=BG)
    d.line([(pad, H - band_h), (W - pad, H - band_h)], fill=GRID, width=2)
    try:
        fk = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
        ft = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 44)
        fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    except Exception:
        fk = ft = fs = ImageFont.load_default()
    y0 = H - band_h + 28
    d.text((pad + 6, y0), f"THE TIER FILES  \u00b7  PART {part}", fill=HIGHLIGHT, font=fk)
    d.text((pad + 6, y0 + 42), title, fill=INK, font=ft)
    if subtitle:
        d.text((pad + 6, y0 + 104), subtitle, fill=SECONDARY, font=fs)
    d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill=MUTED, font=fs)
    cover.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(ROOT))


# --- Part 5: claim layers -------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8.2)
ax.axis("off")
ax.set_title("Who gets to claim the tonne: three paper objects",
             loc="left", fontsize=14, fontweight="bold", color=INK, pad=8)

layers = [
    ("1  ERA / provincial program claim",
     "Portfolio KPI language: funded reductions booked toward Alberta climate results",
     HIGHLIGHT),
    ("2  Alberta Emission Offset Registry",
     "Verified AEOR serials: TIER compliance instruments inside Alberta",
     SECONDARY),
    ("3  BC biomethane environmental attributes",
     "FortisBC BPAs / GGRR: reductions booked into British Columbia climate machinery",
     INK),
]
y = 6.1
for head, sub, accent in layers:
    ax.add_patch(FancyBboxPatch((0.55, y), 8.9, 1.7, boxstyle="square,pad=0",
                                linewidth=1, edgecolor=GRID, facecolor=WASH))
    ax.add_patch(FancyBboxPatch((0.55, y), 0.14, 1.7, boxstyle="square,pad=0",
                                linewidth=0, facecolor=accent))
    ax.text(0.95, y + 1.12, head, fontsize=12, fontweight="bold", color=accent, va="center")
    ax.text(0.95, y + 0.48, sub, fontsize=9.5, color=INK, va="center")
    y -= 2.15
ax.text(5.0, 0.35, "One physical reduction \u00b7 concurrent claim systems \u00b7 no public mass balance between ledgers",
        ha="center", fontsize=9.5, style="italic", color=SECONDARY)
save(fig, P5 / "p5-claim-layers.png",
     "Source: ERA guidelines, AEOR listings, BCUC orders. thesenseofnonsense.com")

# --- Part 6: edge types ---------------------------------------------------
cats = [
    ("ERA / CCEMC funding recipient", 11),
    ("ERA board / chair role", 9),
    ("Employment / executive tenure", 8),
    ("Venture / financing role", 5),
    ("CRIN commercial / board link", 2),
    ("Government / appointment", 2),
    ("Other documented link", 2),
    ("Database intersection (no hit)", 2),
    ("Management-owned company fees", 1),
    ("Decision-date confirmation", 1),
    ("Lobbyist registration", 1),
]
fig, ax = plt.subplots(figsize=(10, 5.8))
style_ax(ax, "44 sourced edges, by relationship type")
labels = [c[0] for c in cats][::-1]
vals = [c[1] for c in cats][::-1]
colors = [MUTED_LIGHT] * len(vals)
for i in range(len(vals) - 4, len(vals)):
    colors[i] = HIGHLIGHT if i == len(vals) - 1 else SECONDARY
ax.barh(labels, vals, color=colors, height=0.62)
ax.set_xlim(0, 13)
ax.set_xlabel("Number of edges")
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for i, v in enumerate(vals):
    ax.text(v + 0.15, i, str(v), va="center", fontsize=9, fontweight="bold", color=INK)
save(fig, P6 / "p6-edge-types.png",
     "Source: ERA / OAG public records. thesenseofnonsense.com")

# --- Part 6: pipeline schematic --------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.0))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.4)
ax.axis("off")
ax.set_title("The pipeline: funded ecosystem to the boardroom",
             loc="left", fontsize=14, fontweight="bold", color=INK, pad=8)

boxes = [
    (0.55, 3.2, "Builders / funders", "funded cos \u00b7 VC portfolios\nemployers \u00b7 partners", WASH),
    (3.85, 3.2, "People in the file", "16 named individuals\nin the edge list", "#FBEAEA"),
    (7.15, 3.2, "ERA board", "directors \u00b7 chairs\nretrospective & concurrent", WASH),
]
for x, y, head, sub, face in boxes:
    ax.add_patch(FancyBboxPatch((x, y), 2.3, 1.9, boxstyle="square,pad=0",
                                linewidth=1.2, edgecolor=GRID, facecolor=face))
    ax.text(x + 1.15, y + 1.38, head, ha="center", fontsize=11.5, fontweight="bold", color=INK)
    ax.text(x + 1.15, y + 0.62, sub, ha="center", fontsize=8.5, color=SECONDARY, linespacing=1.4)
for x0 in (2.95, 6.25):
    ax.add_patch(FancyArrowPatch((x0, 4.15), (x0 + 0.8, 4.15),
                                 arrowstyle="-|>", mutation_scale=18,
                                 linewidth=2, color=HIGHLIGHT))

ax.add_patch(FancyBboxPatch((0.55, 0.7), 8.9, 1.7, boxstyle="square,pad=0",
                            linewidth=1, edgecolor=GRID, facecolor=BG))
stats = [("44 edges", "sourced links"), ("16 people", "in the map"), ("27 orgs", "companies & agencies")]
for i, (big, small) in enumerate(stats):
    cx = 2.05 + i * 2.95
    ax.text(cx, 1.85, big, ha="center", fontsize=15, fontweight="bold", color=HIGHLIGHT)
    ax.text(cx, 1.15, small, ha="center", fontsize=9, color=SECONDARY)
save(fig, P6 / "p6-pipeline.png",
     "Source: ERA / OAG public records. thesenseofnonsense.com")

# --- Part 7: two eras ------------------------------------------------------
years = ["'10", "'11", "'12", "'13", "'14", "'15", "'16", "'17",
         "'18", "'19", "'20", "'21", "'22", "'23", "'24", "'25"]
vals = [2.65, 3.35, 4.31, 5.86, 6.84, None, 4.31, 4.38,
        0.30, 0.29, 0.29, 0.29, 0.29, 0.33, 0.30, 0.32]
fig, ax = plt.subplots(figsize=(10.5, 5.6))
style_ax(ax, "One note, two eras")
xs = range(len(years))
for i, v in enumerate(vals):
    if v is None:
        ax.text(i, 0.12, "n/p", ha="center", fontsize=8, color=MUTED)
        continue
    color = SECONDARY if i <= 7 else HIGHLIGHT
    ax.bar(i, v, 0.62, color=color)
    ax.text(i, v + 0.12, f"{v:.2f}", ha="center", fontsize=7.5, color=INK,
            fontweight="bold" if i > 7 else "normal")
# 7.07 as first reported, dashed outline over the restated '13 bar
ax.bar(3, 7.07, 0.62, fill=False, edgecolor=MUTED, linestyle="--", linewidth=1.2)
ax.text(3, 7.22, "7.07 as first reported", ha="center", fontsize=8, color=MUTED)
ax.annotate(
    "FY2018 statements restate the 2017\ncomparative to $0.32M, a 93% cut,\nwith no reconciliation",
    xy=(7.6, 0.6), xytext=(9.2, 4.6),
    fontsize=9, color=HIGHLIGHT, linespacing=1.4,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.3),
)
ax.set_xticks(list(xs))
ax.set_xticklabels(years)
ax.set_ylabel("$ millions, fees disclosed in the note")
ax.set_ylim(0, 8.2)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.text(3.5, -1.25, "contract management era: the whole function, outsourced",
        ha="center", fontsize=9, color=SECONDARY, transform=ax.transData, clip_on=False)
ax.text(11.5, -1.25, '"companies owned by senior management"',
        ha="center", fontsize=9, color=HIGHLIGHT, transform=ax.transData, clip_on=False)
save(fig, P7 / "p7-two-eras.png",
     "Source: CCEMC/ERA audited statements, remuneration notes. FY2015 not published (n/p). thesenseofnonsense.com")

# --- Covers ----------------------------------------------------------------
make_cover(P6 / "p6-edge-types.png", P6 / "cover.png", 6, "Small World",
           "Board seats, funded companies, Trusted Partners")
make_cover(P7 / "p7-two-eras.png", P7 / "cover.png", 7, "Companies the Board Pays Itself",
           "Fifteen years of one remuneration note")
print("done")
