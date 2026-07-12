"""Regenerate The TIER Files charts — red/grey palette, article-column readable."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "content" / "series" / "the-tier-files"

BG = "#FFFFFF"
WASH = "#F3F3F2"
INK = "#3C3D3C"
MUTED = "#8B8783"
MUTED_LIGHT = "#C5C3C0"
HIGHLIGHT = "#DE0000"
SECONDARY = "#525252"
GRID = "#D6D4D1"
SOURCE = "Source: audited statements / AEPA & ERA public filings. thesenseofnonsense.com"

# Sized for ~680px article width: ~10" wide figures keep labels readable without overflow
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
    ax.title.set_fontfamily("DejaVu Sans")


def save(fig, path: Path):
    fig.patch.set_facecolor(BG)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.012, SOURCE, fontsize=8, color=MUTED)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def make_cover(chart_path: Path, out: Path, part: int, title: str):
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
    d.text((pad + 6, y0), f"THE TIER FILES  ·  PART {part}", fill=HIGHLIGHT, font=fk)
    d.text((pad + 6, y0 + 42), title, fill=INK, font=ft)
    d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill=MUTED, font=fs)
    cover.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(ROOT))


def labeled_box(ax, x, y, w, h, text, face, tc=INK, fs=8.5):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="square,pad=0",
        linewidth=1, edgecolor=GRID, facecolor=face,
    ))
    ax.text(
        x + w / 2, y + h / 2, text,
        ha="center", va="center", fontsize=fs,
        fontweight="bold", color=tc, linespacing=1.25,
    )


# --- Part 1 ---
p1 = SERIES / "part-1-the-billion-dollar-detour"

years = ["FY2022", "FY2023", "FY2024", "FY2025"]
grants = np.array([205.1, 181.1, 94.3, 109.4])
grf = np.array([311.9, 335.5, 416.7, 24.7])
fig, ax = plt.subplots(figsize=(10, 5.2))
style_ax(ax, "General-revenue transfers exceeded grants every year")
x = np.arange(len(years))
w = 0.55
ax.bar(x, grants, w, label="Innovation & technology grants", color=MUTED)
ax.bar(x, grf, w, bottom=grants, label="Transfers to General Revenue Fund", color=HIGHLIGHT)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("\\$ millions")
ax.set_ylim(0, 560)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper right", fontsize=9)
for i, (g, t) in enumerate(zip(grants, grf)):
    if t > 80:
        ax.text(i, g + t / 2, f"{t:.0f}", ha="center", va="center",
                color=BG, fontsize=9, fontweight="bold")
save(fig, p1 / "tier-fund-flow.png")

fig, ax = plt.subplots(figsize=(10, 4.4))
style_ax(ax, "\\$1.85 to general revenue per dollar granted")
vals = [590.0, 1088.8]
labs = [
    "Innovation & technology grants\n\\$590M (4-year)",
    "Transfers to General Revenue Fund\n\\$1,089M (4-year)",
]
cols = [MUTED, HIGHLIGHT]
ax.barh([1, 0], vals, color=cols, height=0.55)
ax.set_xlim(0, 1300)
ax.set_yticks([])
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.set_xlabel("\\$ millions")
ax.text(30, 1, labs[0], va="center", color=INK, fontsize=10, fontweight="bold")
ax.text(30, 0, labs[1], va="center", color=BG, fontsize=10, fontweight="bold")
ax.annotate(
    "1.85×", xy=(1088.8, 0.35), xytext=(720, 0.55),
    fontsize=13, fontweight="bold", color=HIGHLIGHT,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.4),
)
save(fig, p1 / "p1-ratio.png")

fig, ax = plt.subplots(figsize=(10, 5.0))
style_ax(ax, "TIER Fund accumulated surplus tripled to \\$1.1B")
ys = ["FY2022", "FY2023", "FY2024", "FY2025"]
surplus = [336.8, 591.8, 1016.6, 1105.4]
ax.fill_between(ys, surplus, color=HIGHLIGHT, alpha=0.18)
ax.plot(ys, surplus, color=HIGHLIGHT, linewidth=2.4, marker="o", markersize=5)
ax.set_ylim(0, 1300)
ax.set_ylabel("\\$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_ in zip(ys, surplus):
    ax.annotate(
        f"\\${y_:,.0f}M", (x_, y_), textcoords="offset points", xytext=(0, 8),
        ha="center", fontsize=9, color=INK,
    )
save(fig, p1 / "tier-surplus.png")

fig, ax = plt.subplots(figsize=(10, 5.0))
style_ax(ax, "Compliance revenue collapsed 76% in FY2025")
rev = [709.4, 772.1, 936.2, 223.3]
cols = [MUTED, MUTED, MUTED, HIGHLIGHT]
ax.bar(ys, rev, color=cols, width=0.6)
ax.set_ylim(0, 1100)
ax.set_ylabel("\\$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_ in zip(ys, rev):
    ax.text(x_, y_ + 28, f"\\${y_:,.0f}M", ha="center", fontsize=9, color=INK, fontweight="bold")
ax.annotate(
    "−76%", xy=(3, 223), xytext=(2.15, 520),
    fontsize=12, fontweight="bold", color=HIGHLIGHT,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT),
)
save(fig, p1 / "tier-revenue.png")

# sector revenue (from TIER Fund statements of operations)
fig, ax = plt.subplots(figsize=(10, 5.4))
style_ax(ax, "Who actually pays into the TIER Fund")
sectors = ["Mining, oil & gas", "Utilities", "Manufacturing", "Transportation"]
fy_labels = ["FY2022", "FY2023", "FY2024", "FY2025"]
# Rounded from audited sector lines (AEPA annual reports 2022-23 to 2024-25)
sector_data = np.array([
    [248, 384, 454, 97],   # mining
    [389, 237, 330, 25],   # utilities
    [52, 56, 91, 17],      # manufacturing
    [17, 87, 32, 32],      # transportation
], dtype=float)
x = np.arange(len(fy_labels))
n = len(sectors)
width = 0.18
palette = [SECONDARY, HIGHLIGHT, MUTED, MUTED_LIGHT]  # mining, utilities (story), mfg, transport
for i, (name, row) in enumerate(zip(sectors, sector_data)):
    offset = (i - (n - 1) / 2) * width
    ax.bar(x + offset, row, width, label=name, color=palette[i])
    for xi, yi in zip(x + offset, row):
        if yi >= 25:
            ax.text(xi, yi + 8, f"{yi:.0f}", ha="center", va="bottom", fontsize=7, color=INK)
ax.set_xticks(x)
ax.set_xticklabels(fy_labels)
ax.set_ylabel("\\$ millions")
ax.set_ylim(0, 520)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper right")
save(fig, p1 / "p1-sectors.png")

# FY2025 budget vs actual
fig, ax = plt.subplots(figsize=(10, 5.0))
style_ax(ax, "FY2025: the plan versus the year")
cats = ["Revenue", "Innovation grants", "Transfers to\nGeneral Revenue"]
budget = [539, 295, 227]
actual = [223, 109, 25]
x = np.arange(len(cats))
ax.bar(x - 0.18, budget, 0.36, color=MUTED, label="FY2025 budget")
ax.bar(x + 0.18, actual, 0.36, color=HIGHLIGHT, label="FY2025 actual")
ax.set_xticks(x)
ax.set_xticklabels(cats)
ax.set_ylabel("\\$ millions")
ax.set_ylim(0, 620)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9)
for xi, b, a in zip(x, budget, actual):
    ax.text(xi - 0.18, b + 10, f"{b}", ha="center", fontsize=8, color=INK)
    ax.text(xi + 0.18, a + 10, f"{a}", ha="center", fontsize=8, color=INK, fontweight="bold")
save(fig, p1 / "p1-budget-actual.png")

# Path diagram — roomy figure, compact box type
fig, ax = plt.subplots(figsize=(11, 6.4))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.text(
    2, 96, "Where a compliance dollar goes — grants are the minority path",
    fontsize=13, fontweight="bold", color=INK, ha="left",
)
labeled_box(ax, 34, 80, 32, 10, "Regulated facility\npays fund credit", WASH, fs=9)
labeled_box(ax, 34, 64, 32, 10, "TIER Fund\n\\$2.64B collected (4 yrs)", MUTED_LIGHT, fs=9)
labeled_box(ax, 3, 40, 28, 12, "Grants\n\\$590M (~22%)", MUTED, fs=9)
labeled_box(ax, 36, 40, 28, 12, "General revenue\n\\$1,089M (~41%)", HIGHLIGHT, BG, fs=9)
labeled_box(ax, 69, 40, 28, 12, "Held as surplus\n\\$1,105M end FY2025", SECONDARY, BG, fs=9)
labeled_box(ax, 3, 18, 28, 11, "Mostly ERA &\nother delivery agents", WASH, fs=8)
labeled_box(ax, 36, 18, 28, 11, "Indistinguishable from\ntax / royalty once in", WASH, fs=8)
labeled_box(ax, 69, 18, 28, 11, "Not granted.\nNot transferred.", WASH, fs=8)
for a, b in [
    ((50, 80), (50, 74)),
    ((50, 64), (17, 52)),
    ((50, 64), (50, 52)),
    ((50, 64), (83, 52)),
    ((17, 40), (17, 29)),
    ((50, 40), (50, 29)),
    ((83, 40), (83, 29)),
]:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.3))
save(fig, p1 / "p1-path.png")
make_cover(p1 / "p1-ratio.png", p1 / "cover.png", 1, "The Billion-Dollar Detour")

# --- Part 2 ---
p2 = SERIES / "part-2-the-eight-million-dollar-regulator"
yrs = ["2022-23", "2023-24", "2024-25", "2025-26", "2026-27"]
voted = [10.541, 10.541, 10.541, 10.541, 10.541]
actual = [7.097, 7.468, 8.204, 10.541, None]
fig, ax = plt.subplots(figsize=(10, 5.2))
style_ax(ax, "Program 9.1 budget frozen at \\$10.541M for five years")
x = np.arange(len(yrs))
ax.bar(x - 0.18, voted, 0.36, color=MUTED, label="Voted budget")
for i, a in enumerate(actual):
    if a is None:
        continue
    color = HIGHLIGHT if i < 3 else MUTED_LIGHT
    ax.bar(i + 0.18, a, 0.36, color=color, label="Actual / forecast" if i == 0 else None)
ax.set_xticks(x)
ax.set_xticklabels(yrs)
ax.set_ylabel("\\$ millions")
ax.set_ylim(0, 13.5)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9)
ax.annotate(
    "Copy-paste line", xy=(2, 10.541), xytext=(3.05, 12.2),
    fontsize=9, color=HIGHLIGHT,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT),
)
save(fig, p2 / "p2-frozen-line.png")

fig, ax = plt.subplots(figsize=(10, 5.0))
style_ax(ax, "The cheque-writer out-budgets the referee every year")
labels = ["FY2022", "FY2023", "FY2024", "FY2025"]
reg = [7.1, 7.5, 8.2, 8.2]
era = [9.8, 9.5, 9.9, 11.4]
x = np.arange(len(labels))
ax.bar(x - 0.18, reg, 0.36, color=MUTED, label="AEPA program 9.1 (actual)")
ax.bar(x + 0.18, era, 0.36, color=HIGHLIGHT, label="ERA operating expenses")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("\\$ millions")
ax.set_ylim(0, 14)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9)
ax.text(
    0.01, -0.12,
    "Fiscal years differ by ~2 months (AEPA Mar 31; ERA May 31).",
    transform=ax.transAxes, fontsize=8, color=MUTED,
)
save(fig, p2 / "p2-referee-vs-bank.png")

fig, ax = plt.subplots(figsize=(10, 5.4))
style_ax(ax, "The regulatory branch is a rounding error beside the money it polices")
items = [
    ("TIER Fund revenue, FY2024", 936.2),
    ("ERA cash & GICs, May 2025", 539.5),
    ("ERA interest income, FY2025", 25.6),
    ("ERA operating overhead, FY2025", 11.4),
    ("Entire climate regulatory branch, FY2025", 8.2),
]
labs = [i[0] for i in items]
vals = [i[1] for i in items]
cols = [MUTED, MUTED, MUTED, MUTED, HIGHLIGHT]
y = np.arange(len(items))
ax.barh(y, vals, color=cols, height=0.55)
ax.set_yticks(y)
ax.set_yticklabels(labs, fontsize=9)
ax.invert_yaxis()
ax.set_xlim(0, 1150)
ax.set_xlabel("\\$ millions")
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for yi, v in zip(y, vals):
    ax.text(v + 15, yi, f"\\${v:,.1f}M", va="center", fontsize=9, color=INK)
save(fig, p2 / "p2-scale.png")
make_cover(p2 / "p2-scale.png", p2 / "cover.png", 2, "The Eight-Million-Dollar Regulator")

# --- Part 3 ---
p3 = SERIES / "part-3-the-climate-fund-that-became-a-bank"
fig, ax = plt.subplots(figsize=(10, 5.2))
style_ax(ax, "ERA holds ~7.5 years of disbursements in cash and GICs")
fy = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
hold = [510.6, 512.3, 440.9, 487.6, 539.5]
disb = [44.0, 100.7, 84.4, 84.3, 71.7]
ax.plot(fy, hold, color=HIGHLIGHT, linewidth=2.4, marker="o", label="Cash & investments")
ax.bar(fy, disb, color=MUTED, width=0.45, label="Project disbursements")
ax.set_ylim(0, 680)
ax.set_ylabel("\\$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9)
ax.annotate(
    "\\$539.5M held", xy=(4, 539.5), xytext=(2.4, 610),
    fontsize=9, color=HIGHLIGHT,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT),
)
save(fig, p3 / "p3-holdings.png")

fig, ax = plt.subplots(figsize=(10, 5.0))
style_ax(ax, "Interest income topped half of grant revenue in FY2024")
interest = [4.6, 5.3, 19.2, 29.7, 25.6]
cols = [MUTED, MUTED, MUTED, HIGHLIGHT, MUTED]
ax.bar(fy, interest, color=cols, width=0.55)
ax.set_ylim(0, 38)
ax.set_ylabel("\\$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_ in zip(fy, interest):
    ax.text(x_, y_ + 0.7, f"\\${y_:.1f}M", ha="center", fontsize=9, color=INK, fontweight="bold")
ax.annotate(
    "Over half of grant revenue\n($51.9M)", xy=(3, 29.7), xytext=(1.2, 33),
    fontsize=9, color=HIGHLIGHT,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT),
)
save(fig, p3 / "p3-interest.png")

fig, ax = plt.subplots(figsize=(11, 5.8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.text(
    2, 94, "The ladder is the strategy: maturities run into 2027",
    fontsize=13, fontweight="bold", color=INK,
)
rows = [
    ("Cash", "\\$309.5M", "Demand deposits"),
    ("Short-term GICs", "\\$40.0M", "Scotiabank & CWB · 4.54–5.49%"),
    ("Long-term GICs", "\\$190.0M", "Scotiabank & ATB · 3.75–4.14% · Nov 2026–Apr 2027"),
    ("Total holdings", "\\$539.5M", "As of May 31, 2025 (Note 5)"),
]
y = 78
for i, (a, b, c) in enumerate(rows):
    face = HIGHLIGHT if i == 3 else WASH
    tc = BG if i == 3 else INK
    ax.add_patch(FancyBboxPatch(
        (3, y - 7), 94, 13, boxstyle="square,pad=0",
        facecolor=face, edgecolor=GRID, linewidth=1,
    ))
    ax.text(6, y - 0.5, a, fontsize=10, fontweight="bold", color=tc, va="center")
    ax.text(32, y - 0.5, b, fontsize=11, fontweight="bold", color=tc, va="center")
    ax.text(48, y - 0.5, c, fontsize=9, color=tc if i == 3 else SECONDARY, va="center")
    y -= 16
ax.text(
    3, 8,
    "Amounts shown as disclosed aggregates; Note 5 does not break GICs per institution.",
    fontsize=8, color=MUTED,
)
save(fig, p3 / "p3-ladder.png")
make_cover(p3 / "p3-holdings.png", p3 / "cover.png", 3, "The Climate Fund That Became a Bank")

# --- Part 4 ---
p4 = SERIES / "part-4-the-float"
fig, ax = plt.subplots(figsize=(10, 5.2))
style_ax(ax, "Sixteen years of payouts sit far below the \\$1.17B commitment")
annual = [0, 0.1, 23, 22, 37.1, 30, 28, 21.7, 34.1, 33.6, 38.2, 44, 100.7, 84.4, 84.3, 71.7]
cum = np.cumsum(annual)
years_n = list(range(2010, 2026))
ax.plot(years_n, cum, color=HIGHLIGHT, linewidth=2.4, label="Cumulative project expenses")
ax.axhline(1170, color=MUTED, linestyle="--", linewidth=1.5, label="\\$1.17B committed (headline)")
ax.set_ylim(0, 1400)
ax.set_ylabel("\\$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=9)
ax.annotate(
    f"~\\${cum[-1]:.0f}M paid", xy=(2025, cum[-1]), xytext=(2015, 900),
    fontsize=9, color=HIGHLIGHT,
    arrowprops=dict(arrowstyle="->", color=HIGHLIGHT),
)
save(fig, p4 / "era-float.png")

fig, ax = plt.subplots(figsize=(10, 5.2))
style_ax(ax, "FY2025: ERA un-funded more (\\$82.7M) than it paid out (\\$71.7M)")
cy = ["FY2022", "FY2023", "FY2024", "FY2025"]
canc = [19.9, 22.6, 53.8, 82.7]
cols = [MUTED, MUTED, MUTED, HIGHLIGHT]
ax.bar(cy, canc, color=cols, width=0.55)
ax.axhline(71.7, color=SECONDARY, linestyle="--", linewidth=1.4)
ax.text(3.28, 74, "Paid out FY2025\n\\$71.7M", fontsize=8, color=SECONDARY, ha="left")
ax.set_ylim(0, 100)
ax.set_ylabel("\\$ millions cancelled / terminated")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_ in zip(cy, canc):
    ax.text(x_, y_ + 2.2, f"\\${y_:.1f}M", ha="center", fontsize=9, fontweight="bold", color=INK)
save(fig, p4 / "p4-cancellations.png")

fig, ax = plt.subplots(figsize=(11, 6.4))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.text(
    2, 96, "Lifecycle of an announced dollar — most never leave as a finished project",
    fontsize=12, fontweight="bold", color=INK,
)
labeled_box(ax, 6, 74, 26, 12, "Announcement &\ncontribution agreement", WASH, fs=9)
labeled_box(ax, 37, 74, 26, 12, "Float\n(cash + GIC ladder)", MUTED_LIGHT, fs=9)
labeled_box(ax, 68, 74, 26, 12, "Milestone payments\n~55–60¢ / \\$", MUTED, fs=9)
labeled_box(ax, 37, 44, 26, 12, "Quiet death\ncancel / terminate / On Hold", HIGHLIGHT, BG, fs=9)
labeled_box(ax, 6, 16, 26, 12, "Re-announce\nin new challenge", WASH, fs=9)
labeled_box(ax, 37, 16, 26, 12, "Interest clawback\n/ netting", WASH, fs=9)
labeled_box(ax, 68, 16, 26, 12, "Direct reallocation\nby ministry", WASH, fs=9)
for a, b in [
    ((32, 80), (37, 80)),
    ((63, 80), (68, 80)),
    ((50, 74), (50, 56)),
    ((37, 50), (19, 28)),
    ((50, 44), (50, 28)),
    ((63, 50), (81, 28)),
]:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.3))
save(fig, p4 / "p4-lifecycle.png")
make_cover(p4 / "p4-cancellations.png", p4 / "cover.png", 4, "The Float")

# Keep series landing card in sync
import shutil
shutil.copy2(p1 / "cover.png", SERIES / "cover.png")
print("wrote", (SERIES / "cover.png").relative_to(ROOT))
print("done")
