"""Ghost Lives editorial figures - replaces the comic panels.

Generates chart/diagram figures in the site red/grey style (matching
regen-tier-charts.py) plus new covers for Part 2 and the series landing.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "content" / "series" / "ghost-lives"
P1 = SERIES / "part-1-what-the-premium-buys"
P2 = SERIES / "part-2-where-stacking-ends"

BG = "#FFFFFF"
WASH = "#F3F3F2"
INK = "#3C3D3C"
MUTED = "#8B8783"
MUTED_LIGHT = "#C5C3C0"
HIGHLIGHT = "#DE0000"
SECONDARY = "#525252"
GRID = "#D6D4D1"
RED_WASH = "#FBEAEA"
SOURCE = "Source: BCUC / FEI filings summarised in Ghost Lives. thesenseofnonsense.com"

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


def save(fig, path: Path, source: str = SOURCE):
    fig.patch.set_facecolor(BG)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.012, source, fontsize=8, color=MUTED)
    fig.savefig(path, dpi=180, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def box(ax, x, y, w, h, head, sub, face=WASH, edge=GRID, head_color=INK, lw=1.2,
        head_fs=10.5, sub_fs=8.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                linewidth=lw, edgecolor=edge, facecolor=face))
    if sub:
        ax.text(x + w / 2, y + h * 0.66, head, ha="center", va="center",
                fontsize=head_fs, fontweight="bold", color=head_color)
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center",
                fontsize=sub_fs, color=SECONDARY, linespacing=1.35)
    else:
        ax.text(x + w / 2, y + h / 2, head, ha="center", va="center",
                fontsize=head_fs, fontweight="bold", color=head_color)


def arrow(ax, x0, y0, x1, y1, color=SECONDARY, lw=1.8):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>",
                                 mutation_scale=15, linewidth=lw, color=color))


# --- P1: blend floor + premium ---------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5.0))
style_ax(ax, "The renewable floor climbs; every customer pays")
dates = ["1 Jul 2024", "1 Jul 2025", "1 Jul 2026"]
blend = [1.0, 3.0, 3.5]
cols = [MUTED, SECONDARY, HIGHLIGHT]
ax.bar(dates, blend, 0.5, color=cols)
for x_, y_ in zip(dates, blend):
    ax.text(x_, y_ + 0.09, f"{y_:g}%", ha="center", fontsize=11, fontweight="bold", color=INK)
ax.set_ylim(0, 4.6)
ax.set_ylabel("Designated (mandatory) renewable blend")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.text(0.02, 0.95,
        "Voluntary premium on top: $7/GJ ordered in G-77-24;\ncompany page shows $8.660/GJ as of 1 April 2026",
        transform=ax.transAxes, fontsize=9.5, color=SECONDARY, va="top", linespacing=1.4)
save(fig, P1 / "p1-blend-premium.png")

# --- P1: where the premium dollar sits --------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 7)
ax.axis("off")
ax.set_title("One acquisition, three revenue doors", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=8)

box(ax, 0.5, 4.9, 2.6, 1.5, "Customer premium", "$7-$8.66 / GJ\nvoluntary designation", RED_WASH, HIGHLIGHT, HIGHLIGHT)
box(ax, 0.5, 2.75, 2.6, 1.5, "Mandatory blend", "3.5% on every bill\nrate mechanisms")
box(ax, 4.0, 3.8, 2.5, 1.6, "FEI RNG acquisition", "attributes 'retired'\nby internal volume\naccounting")
box(ax, 7.3, 5.0, 2.3, 1.4, "Carbon-tax refund", "claimed from the\nProvince on sale")
box(ax, 7.3, 3.05, 2.3, 1.4, "CFR credit share", "side letters split credits\nwith suppliers")
box(ax, 7.3, 1.1, 2.3, 1.4, "RNG Account", "FEI's share of proceeds\nreduces rates")
arrow(ax, 3.1, 5.55, 4.0, 4.9)
arrow(ax, 3.1, 3.5, 4.0, 4.3)
arrow(ax, 6.5, 4.95, 7.3, 5.55, HIGHLIGHT)
arrow(ax, 6.5, 4.5, 7.3, 3.85, HIGHLIGHT)
arrow(ax, 8.45, 3.05, 8.45, 2.5, MUTED)
ax.text(5.0, 0.4, "Every arrow is described in FortisBC's own Commission filings.",
        ha="center", fontsize=9.5, style="italic", color=SECONDARY)
save(fig, P1 / "p1-ratepayer-dollar.png")

# --- P2: the gram's journey --------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 6.0))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7.4)
ax.axis("off")
ax.set_title("One gram of CO2e, every ledger that claims it", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=8)

top = [
    (0.4, 4.6, "Manure lagoon", "methane would\nhave vented"),
    (3.4, 4.6, "Digester", "captured, upgraded\nto biomethane"),
    (6.4, 4.6, "Alberta scoreboard", "funded tonne stays\non program claims"),
    (9.4, 4.6, "Hub displacement", "attribute paired with\nconventional gas"),
]
for i, (x, y, head, sub) in enumerate(top):
    face = WASH if i != 2 else RED_WASH
    box(ax, x, y, 2.3, 1.7, head, sub, face)
    if i < 3:
        arrow(ax, x + 2.3, y + 0.85, x + 3.0, y + 0.85)

bottom = [
    (9.4, 1.4, "BC bill + tax refund", "'retired' to ratepayer;\nProvince refunds tax"),
    (6.4, 1.4, "Federal CFR credit", "sold to a gasoline or\ndiesel supplier"),
    (3.4, 1.4, "BC LCFS credit", "if eligible CNG\ntransportation use"),
]
for i, (x, y, head, sub) in enumerate(bottom):
    box(ax, x, y, 2.3, 1.7, head, sub, RED_WASH, HIGHLIGHT, HIGHLIGHT)
    if i < 2:
        arrow(ax, x, y + 0.85, x - 0.7, y + 0.85, HIGHLIGHT)
arrow(ax, 10.55, 4.6, 10.55, 3.1, HIGHLIGHT)
ax.text(6.0, 0.45, "Top row: the physical event and Alberta's claim. Bottom row: what the same attribute can still fund.",
        ha="center", fontsize=9.5, style="italic", color=SECONDARY)
save(fig, P2 / "p2-journey.png")

# --- P2: three grams, three systems ------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 5.4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8.2)
ax.axis("off")
ax.set_title("Three paper objects people call 'a tonne'", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=8)
layers = [
    ("Gram A  \u00b7  Inventory carbon",
     "IPCC territorial method: combustion counts where it happens; production counts where it happened",
     SECONDARY),
    ("Gram B  \u00b7  Alberta program carbon",
     "TIER, AEOR serials, ERA portfolio megatonnes: compliance and KPI objects in Alberta's accounts",
     INK),
    ("Gram C  \u00b7  Clean Fuel Regulations carbon",
     "Lifecycle object: one CFR credit equals one tonne CO2e, tradable to liquid-fuel suppliers",
     HIGHLIGHT),
]
y = 6.0
for head, sub, accent in layers:
    box_face = WASH
    ax.add_patch(FancyBboxPatch((0.55, y), 8.9, 1.75, boxstyle="square,pad=0",
                                linewidth=1, edgecolor=GRID, facecolor=box_face))
    ax.add_patch(FancyBboxPatch((0.55, y), 0.14, 1.75, boxstyle="square,pad=0",
                                linewidth=0, facecolor=accent))
    ax.text(0.95, y + 1.18, head, fontsize=11.5, fontweight="bold", color=accent, va="center")
    ax.text(0.95, y + 0.5, sub, fontsize=9, color=INK, va="center")
    y -= 2.2
ax.text(5.0, 0.4, "Ghost lives begin when A, B, and C are treated as separate tonnes in the atmosphere.",
        ha="center", fontsize=9.5, style="italic", color=SECONDARY)
save(fig, P2 / "p2-three-grams.png")

# --- P2: quasi-stacking -------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 4.8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5.6)
ax.axis("off")
ax.set_title("Quasi-stacking: the claim stays, the attribute leaves", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=8)
box(ax, 3.65, 3.0, 2.7, 1.7, "Funded digester", "TIER / ERA capital;\none physical reduction")
box(ax, 0.5, 0.6, 3.6, 1.7, "Stays in Alberta", "program + portfolio claims:\nplan megatonnes, grant KPIs,\nsometimes an AEOR serial", WASH, GRID, INK)
box(ax, 5.9, 0.6, 3.6, 1.7, "Leaves for BC", "marketable environmental\nattribute sold under a\nFortisBC BPA", RED_WASH, HIGHLIGHT, HIGHLIGHT)
arrow(ax, 4.3, 3.0, 2.7, 2.3)
arrow(ax, 5.7, 3.0, 7.3, 2.3, HIGHLIGHT)
ax.text(5.0, 0.06, '"Alberta is supporting emissions reductions in other jurisdictions."  - Alberta\'s own 2023 climate plan, p. 44',
        ha="center", fontsize=9.5, style="italic", color=SECONDARY)
save(fig, P2 / "p2-quasi-stack.png",
     "Source: EREDP 2023; ERA guidelines; BCUC orders. thesenseofnonsense.com")

# --- P2: CFR credit flow ------------------------------------------------------
fig, ax = plt.subplots(figsize=(10.5, 4.8))
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.4)
ax.axis("off")
ax.set_title("Life 4: the federal credit rides a side letter", loc="left",
             fontsize=14, fontweight="bold", color=INK, pad=8)
flow = [
    (0.4, 2.5, "Supplier", "registers the project;\nattests feedstock and CI", WASH, INK),
    (3.4, 2.5, "Side letter with FEI", "credits or revenue split;\nFEI share to RNG Account", WASH, INK),
    (6.4, 2.5, "CFR credit", "one tonne lifecycle CO2e,\ntradable", RED_WASH, HIGHLIGHT),
    (9.4, 2.5, "Refiner / importer", "buys compliance for its\ngasoline and diesel pool", WASH, INK),
]
for i, (x, y, head, sub, face, hc) in enumerate(flow):
    box(ax, x, y, 2.3, 1.8, head, sub, face, GRID, hc)
    if i < 3:
        arrow(ax, x + 2.3, y + 0.9, x + 3.0, y + 0.9, HIGHLIGHT if i >= 1 else SECONDARY)
ax.text(6.0, 1.3, '"Stackable ... is a policy choice, not double counting."  - FortisBC, G-137-25 submission, s. 3.2',
        ha="center", fontsize=9.5, style="italic", color=SECONDARY)
ax.text(6.0, 0.55, "The atmospheric work happened at the lagoon. The compliance work happens on a refiner's ledger.",
        ha="center", fontsize=9.5, color=SECONDARY)
save(fig, P2 / "p2-cfr-flow.png")

# --- Covers -------------------------------------------------------------------
def make_cover(chart_path: Path, out: Path, kicker: str, title: str, subtitle: str = ""):
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
    d.text((pad + 6, y0), kicker, fill=HIGHLIGHT, font=fk)
    d.text((pad + 6, y0 + 42), title, fill=INK, font=ft)
    if subtitle:
        d.text((pad + 6, y0 + 104), subtitle, fill=SECONDARY, font=fs)
    d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill=MUTED, font=fs)
    cover.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(ROOT))


make_cover(P2 / "p2-journey.png", P2 / "cover.png",
           "GHOST LIVES  \u00b7  PART 2", "Where Stacking Ends",
           "One gram, every ledger that claims it")
make_cover(P2 / "p2-ghost-stack.png", SERIES / "cover.png",
           "SERIES", "Ghost Lives",
           "The molecule does one job. The paper lives longer.")
print("done")
