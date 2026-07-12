"""Regenerate The TIER Files charts in McKinsey / light-magazine style."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "content" / "series" / "the-tier-files"

BG = "#FFFFFF"
WASH = "#F7F5F0"
INK = "#1A1A1A"
MUTED = "#B0B0B0"
MUTED_LIGHT = "#D0D0D0"
HIGHLIGHT = "#C45C26"  # Sense of Nonsense brand
SECONDARY = "#4A4A4A"
GRID = "#E8E8E8"
POS = "#2F6F4E"
NEG = "#C45C26"
SOURCE = "Source: audited statements / AEPA & ERA public filings. thesenseofnonsense.com"

plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 20,
    "axes.labelsize": 14,
    "xtick.labelsize": 14,
    "ytick.labelsize": 14,
    "legend.fontsize": 13,
    "figure.titlesize": 18,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
})


def style_ax(ax, title: str):
    ax.set_facecolor(BG)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK, labelsize=14)
    ax.set_title(title, loc="left", fontsize=22, fontweight="bold", color=INK, pad=14)
    ax.title.set_fontfamily("DejaVu Sans")


def save(fig, path: Path):
    fig.patch.set_facecolor(BG)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.text(0.01, 0.012, SOURCE, fontsize=12, color=MUTED)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=200, facecolor=BG, edgecolor="none")
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
    d.line([(pad, H - band_h), (W - pad, H - band_h)], fill="#E6E2DA", width=2)
    try:
        fk = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
        ft = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 48)
        fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    except Exception:
        fk = ft = fs = ImageFont.load_default()
    y0 = H - band_h + 28
    d.text((pad + 6, y0), f"THE TIER FILES  ·  PART {part}", fill=HIGHLIGHT, font=fk)
    d.text((pad + 6, y0 + 42), title, fill=INK, font=ft)
    d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill="#6B6B6B", font=fs)
    cover.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(ROOT))


# --- Part 1 ---
p1 = SERIES / "part-1-the-billion-dollar-detour"

# stacked outflows
years = ["FY2022", "FY2023", "FY2024", "FY2025"]
grants = np.array([205.1, 181.1, 94.3, 109.4])
grf = np.array([311.9, 335.5, 416.7, 24.7])
fig, ax = plt.subplots(figsize=(8.5, 4.6))
style_ax(ax, "General-revenue transfers exceeded grants every year")
x = np.arange(len(years))
w = 0.55
ax.bar(x, grants, w, label="Innovation & technology grants", color=MUTED)
ax.bar(x, grf, w, bottom=grants, label="Transfers to General Revenue Fund", color=HIGHLIGHT)
ax.set_xticks(x)
ax.set_xticklabels(years)
ax.set_ylabel("$ millions")
ax.set_ylim(0, 560)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, loc="upper right", fontsize=15)
for i, (g, t) in enumerate(zip(grants, grf)):
    if t > 80:
        ax.text(i, g + t / 2, f"{t:.0f}", ha="center", va="center", color=BG, fontsize=14, fontweight="bold")
save(fig, p1 / "tier-fund-flow.png")

# ratio
fig, ax = plt.subplots(figsize=(8.5, 3.8))
style_ax(ax, "$1.85 to general revenue for every dollar granted")
vals = [590.0, 1088.8]
labs = ["Innovation & technology grants\n$590M (4-year)", "Transfers to General Revenue Fund\n$1,089M (4-year)"]
cols = [MUTED, HIGHLIGHT]
ax.barh([1, 0], vals, color=cols, height=0.55)
ax.set_xlim(0, 1300)
ax.set_yticks([])
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.set_xlabel("$ millions")
ax.text(30, 1, labs[0], va="center", color=INK, fontsize=16, fontweight="bold")
ax.text(30, 0, labs[1], va="center", color=BG, fontsize=16, fontweight="bold")
ax.annotate("1.85×", xy=(1088.8, 0.35), xytext=(700, 0.55),
            fontsize=22, fontweight="bold", color=HIGHLIGHT,
            arrowprops=dict(arrowstyle="->", color=HIGHLIGHT, lw=1.5))
save(fig, p1 / "p1-ratio.png")

# surplus
fig, ax = plt.subplots(figsize=(8.5, 4.2))
style_ax(ax, "TIER Fund accumulated surplus tripled to $1.1B")
ys = ["FY2022", "FY2023", "FY2024", "FY2025"]
surplus = [336.8, 591.8, 1016.6, 1105.4]
ax.fill_between(ys, surplus, color=HIGHLIGHT, alpha=0.18)
ax.plot(ys, surplus, color=HIGHLIGHT, linewidth=2.6, marker="o", markersize=6)
ax.set_ylim(0, 1300)
ax.set_ylabel("$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_ in zip(ys, surplus):
    ax.annotate(f"${y_:,.0f}M", (x_, y_), textcoords="offset points", xytext=(0, 10),
                ha="center", fontsize=14, color=INK)
save(fig, p1 / "tier-surplus.png")

# revenue collapse
fig, ax = plt.subplots(figsize=(8.5, 4.2))
style_ax(ax, "Compliance revenue collapsed 76% in FY2025")
rev = [709.4, 772.1, 936.2, 223.3]
cols = [MUTED, MUTED, MUTED, HIGHLIGHT]
ax.bar(ys, rev, color=cols, width=0.6)
ax.set_ylim(0, 1100)
ax.set_ylabel("$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_, c in zip(ys, rev, cols):
    ax.text(x_, y_ + 25, f"${y_:,.0f}M", ha="center", fontsize=15, color=INK, fontweight="bold")
ax.annotate("−76%", xy=(3, 223), xytext=(2.2, 500), fontsize=18, fontweight="bold",
            color=HIGHLIGHT, arrowprops=dict(arrowstyle="->", color=HIGHLIGHT))
save(fig, p1 / "tier-revenue.png")

# path diagram (simplified McKinsey boxes)
fig, ax = plt.subplots(figsize=(8.5, 4.7))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.text(2, 94, "Where a compliance dollar goes — grants are the minority path", fontsize=20,
        fontweight="bold", color=INK, ha="left")


def box(x, y, w, h, text, face, tc=INK):
    r = FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", linewidth=1,
                       edgecolor=GRID, facecolor=face)
    ax.add_patch(r)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=16,
            fontweight="bold", color=tc, wrap=True)


box(35, 78, 30, 9, "Regulated facility\npays fund credit", WASH)
box(35, 62, 30, 9, "TIER Fund\n$2.64B collected (4 yrs)", MUTED_LIGHT)
box(4, 38, 28, 12, "Grants\n$590M (~22%)", MUTED)
box(36, 38, 28, 12, "General revenue\n$1,089M (~41%)", HIGHLIGHT, BG)
box(68, 38, 28, 12, "Held as surplus\n$1,105M end FY2025", SECONDARY, BG)
box(4, 18, 28, 10, "Mostly ERA &\nother delivery agents", WASH)
box(36, 18, 28, 10, "Indistinguishable from\ntax / royalty once in", WASH)
box(68, 18, 28, 10, "Not granted.\nNot transferred.", WASH)
for a, b in [((50, 78), (50, 71)), ((50, 62), (18, 50)), ((50, 62), (50, 50)), ((50, 62), (82, 50)),
             ((18, 38), (18, 28)), ((50, 38), (50, 28)), ((82, 38), (82, 28))]:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
save(fig, p1 / "p1-path.png")
make_cover(p1 / "p1-ratio.png", p1 / "cover.png", 1, "The Billion-Dollar Detour")

# --- Part 2 ---
p2 = SERIES / "part-2-the-eight-million-dollar-regulator"
yrs = ["2022-23", "2023-24", "2024-25", "2025-26", "2026-27"]
voted = [10.541, 10.541, 10.541, 10.541, 10.541]
actual = [7.097, 7.468, 8.204, 10.541, None]
fig, ax = plt.subplots(figsize=(8.5, 4.4))
style_ax(ax, "Program 9.1 budget frozen at $10.541M for five years")
x = np.arange(len(yrs))
ax.bar(x - 0.18, voted, 0.36, color=MUTED, label="Voted budget")
act_vals = [a if a is not None else 0 for a in actual]
act_cols = [HIGHLIGHT if a is not None and i < 3 else MUTED_LIGHT for i, a in enumerate(actual)]
# only plot actuals where known; forecast hatched
for i, a in enumerate(actual):
    if a is None:
        continue
    color = HIGHLIGHT if i < 3 else MUTED_LIGHT
    ax.bar(i + 0.18, a, 0.36, color=color, label="Actual / forecast" if i == 0 else None)
ax.set_xticks(x)
ax.set_xticklabels(yrs)
ax.set_ylabel("$ millions")
ax.set_ylim(0, 13)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=15)
ax.annotate("Copy-paste line", xy=(2, 10.541), xytext=(3.1, 12), fontsize=15, color=HIGHLIGHT,
            arrowprops=dict(arrowstyle="->", color=HIGHLIGHT))
save(fig, p2 / "p2-frozen-line.png")

fig, ax = plt.subplots(figsize=(8.5, 4.2))
style_ax(ax, "The cheque-writer out-budgets the referee every year")
labels = ["FY2022", "FY2023", "FY2024", "FY2025"]
reg = [7.1, 7.5, 8.2, 8.2]  # approximate last as actual window
era = [9.8, 9.5, 9.9, 11.4]
x = np.arange(len(labels))
ax.bar(x - 0.18, reg, 0.36, color=MUTED, label="AEPA program 9.1 (actual)")
ax.bar(x + 0.18, era, 0.36, color=HIGHLIGHT, label="ERA operating expenses")
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel("$ millions")
ax.set_ylim(0, 14)
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=15)
ax.text(0.01, -0.14, "Fiscal years differ by ~2 months (AEPA Mar 31; ERA May 31).",
        transform=ax.transAxes, fontsize=13, color=MUTED)
save(fig, p2 / "p2-referee-vs-bank.png")

fig, ax = plt.subplots(figsize=(8.5, 4.6))
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
ax.barh(y, vals, color=cols, height=0.6)
ax.set_yticks(y)
ax.set_yticklabels(labs, fontsize=15)
ax.invert_yaxis()
ax.set_xlim(0, 1100)
ax.set_xlabel("$ millions")
ax.xaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for yi, v in zip(y, vals):
    ax.text(v + 12, yi, f"${v:,.1f}M", va="center", fontsize=14, color=INK)
save(fig, p2 / "p2-scale.png")
make_cover(p2 / "p2-scale.png", p2 / "cover.png", 2, "The Eight-Million-Dollar Regulator")

# --- Part 3 ---
p3 = SERIES / "part-3-the-climate-fund-that-became-a-bank"
fig, ax = plt.subplots(figsize=(8.5, 4.6))
style_ax(ax, "ERA holds ~7.5 years of disbursements in cash and GICs")
fy = ["FY2021", "FY2022", "FY2023", "FY2024", "FY2025"]
hold = [510.6, 512.3, 440.9, 487.6, 539.5]
disb = [44.0, 100.7, 84.4, 84.3, 71.7]
ax.plot(fy, hold, color=HIGHLIGHT, linewidth=2.6, marker="o", label="Cash & investments")
ax.bar(fy, disb, color=MUTED, width=0.45, label="Project disbursements")
ax.set_ylim(0, 650)
ax.set_ylabel("$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=15)
ax.annotate("$539.5M held", xy=(4, 539.5), xytext=(2.5, 600), fontsize=15, color=HIGHLIGHT,
            arrowprops=dict(arrowstyle="->", color=HIGHLIGHT))
save(fig, p3 / "p3-holdings.png")

fig, ax = plt.subplots(figsize=(8.5, 4.2))
style_ax(ax, "Interest income topped half of grant revenue in FY2024")
interest = [4.6, 5.3, 19.2, 29.7, 25.6]
cols = [MUTED, MUTED, MUTED, HIGHLIGHT, MUTED]
ax.bar(fy, interest, color=cols, width=0.55)
ax.set_ylim(0, 36)
ax.set_ylabel("$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_, c in zip(fy, interest, cols):
    ax.text(x_, y_ + 0.8, f"${y_:.1f}M", ha="center", fontsize=14, color=INK, fontweight="bold")
ax.annotate(">$½ of grant revenue\n($51.9M)", xy=(3, 29.7), xytext=(1.5, 32), fontsize=14,
            color=HIGHLIGHT, arrowprops=dict(arrowstyle="->", color=HIGHLIGHT))
save(fig, p3 / "p3-interest.png")

# ladder as statement panel
fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.text(2, 94, "The ladder is the strategy: maturities run into 2027", fontsize=20,
        fontweight="bold", color=INK)
rows = [
    ("Cash", "$309.5M", "Demand deposits"),
    ("Short-term GICs", "$40.0M", "Scotiabank & CWB · 4.54–5.49%"),
    ("Long-term GICs", "$190.0M", "Scotiabank & ATB · 3.75–4.14% · Nov 2026–Apr 2027"),
    ("Total holdings", "$539.5M", "As of May 31, 2025 (Note 5)"),
]
y = 78
for i, (a, b, c) in enumerate(rows):
    face = HIGHLIGHT if i == 3 else WASH
    tc = BG if i == 3 else INK
    ax.add_patch(FancyBboxPatch((4, y - 8), 92, 14, boxstyle="square,pad=0",
                                facecolor=face, edgecolor=GRID, linewidth=1))
    ax.text(8, y - 1, a, fontsize=17, fontweight="bold", color=tc, va="center")
    ax.text(40, y - 1, b, fontsize=18, fontweight="bold", color=tc, va="center")
    ax.text(58, y - 1, c, fontsize=15, color=tc if i == 3 else SECONDARY, va="center")
    y -= 16
ax.text(4, 8, "Amounts shown as disclosed aggregates; Note 5 does not break GICs per institution.",
        fontsize=13, color=MUTED)
save(fig, p3 / "p3-ladder.png")
make_cover(p3 / "p3-holdings.png", p3 / "cover.png", 3, "The Climate Fund That Became a Bank")

# --- Part 4 ---
p4 = SERIES / "part-4-the-float"
fig, ax = plt.subplots(figsize=(8.5, 4.6))
style_ax(ax, "Sixteen years of payouts sit far below the $1.17B commitment")
# approximate cumulative from table
annual = [0, 0.1, 23, 22, 37.1, 30, 28, 21.7, 34.1, 33.6, 38.2, 44, 100.7, 84.4, 84.3, 71.7]
# FY2010-2025; FY2015 estimated ~30
cum = np.cumsum(annual)
years_n = list(range(2010, 2026))
ax.plot(years_n, cum, color=HIGHLIGHT, linewidth=2.6, label="Cumulative project expenses")
ax.axhline(1170, color=MUTED, linestyle="--", linewidth=1.6, label="$1.17B committed (headline)")
ax.set_ylim(0, 1400)
ax.set_ylabel("$ millions")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=15)
ax.annotate(f"~${cum[-1]:.0f}M paid", xy=(2025, cum[-1]), xytext=(2016, 900),
            fontsize=15, color=HIGHLIGHT, arrowprops=dict(arrowstyle="->", color=HIGHLIGHT))
save(fig, p4 / "era-float.png")

fig, ax = plt.subplots(figsize=(8.5, 4.4))
style_ax(ax, "FY2025: ERA un-funded more ($82.7M) than it paid out ($71.7M)")
cy = ["FY2022", "FY2023", "FY2024", "FY2025"]
canc = [19.9, 22.6, 53.8, 82.7]
cols = [MUTED, MUTED, MUTED, HIGHLIGHT]
ax.bar(cy, canc, color=cols, width=0.55)
ax.axhline(71.7, color=SECONDARY, linestyle="--", linewidth=1.5)
ax.text(3.35, 73.5, "Paid out FY2025\n$71.7M", fontsize=14, color=SECONDARY, ha="left")
ax.set_ylim(0, 100)
ax.set_ylabel("$ millions cancelled / terminated")
ax.yaxis.grid(True, color=GRID, linewidth=0.6)
ax.set_axisbelow(True)
for x_, y_ in zip(cy, canc):
    ax.text(x_, y_ + 2, f"${y_:.1f}M", ha="center", fontsize=15, fontweight="bold", color=INK)
save(fig, p4 / "p4-cancellations.png")

# lifecycle flowchart
fig, ax = plt.subplots(figsize=(8.5, 4.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
ax.set_facecolor(BG)
fig.patch.set_facecolor(BG)
ax.text(2, 94, "Lifecycle of an announced dollar — most never leave as a finished project",
        fontsize=20, fontweight="bold", color=INK)


def box2(x, y, w, h, text, face=WASH, tc=INK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0",
                                facecolor=face, edgecolor=GRID, linewidth=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=15,
            fontweight="bold", color=tc)


box2(8, 72, 24, 12, "Announcement &\ncontribution agreement", WASH)
box2(40, 72, 24, 12, "Float\n(cash + GIC ladder)", MUTED_LIGHT)
box2(72, 72, 22, 12, "Milestone\npayments\n~55–60¢ /$", MUTED)
box2(40, 42, 24, 12, "Quiet death\ncancel / terminate / On Hold", HIGHLIGHT, BG)
box2(8, 18, 28, 12, "Re-announce\nin new challenge", WASH)
box2(40, 18, 24, 12, "Interest clawback\n/ netting", WASH)
box2(70, 18, 24, 12, "Direct reallocation\nby ministry", WASH)
for a, b in [((32, 78), (40, 78)), ((64, 78), (72, 78)), ((52, 72), (52, 54)),
             ((40, 48), (22, 30)), ((52, 42), (52, 30)), ((64, 48), (82, 30))]:
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
save(fig, p4 / "p4-lifecycle.png")
make_cover(p4 / "p4-cancellations.png", p4 / "cover.png", 4, "The Float")

print("done")
