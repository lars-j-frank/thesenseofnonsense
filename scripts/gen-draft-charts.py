"""Generate editorial charts for draft TIER Files / essays (saddle-brown palette)."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG = "#FAF9F7"
INK = "#141413"
MUTED = "#333333"
ACCENT = "#8B4513"
WASH = "#E8E4DF"
GRID = "#D6D4D1"
LIGHT = "#C4B8A8"
SOURCE = "Source: ERA / OAG public records. thesenseofnonsense.com"

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
    }
)


def style_ax(ax, title: str) -> None:
    ax.set_facecolor(BG)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK)
    ax.set_title(title, loc="left", fontsize=14, fontweight="bold", color=INK, pad=12)


def save(fig, path: Path) -> None:
    fig.patch.set_facecolor(BG)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.text(0.01, 0.015, SOURCE, fontsize=8, color=MUTED, alpha=0.85)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def edge_category(rel: str) -> str:
    r = (rel or "").lower()
    if (
        "funding recipient" in r
        or "era recipient" in r
        or ("ccemc" in r and "award" in r)
        or "era funding" in r
    ):
        return "ERA / CCEMC funding recipient"
    if any(
        k in r
        for k in (
            "portfolio",
            "partner",
            "investment manager",
            "general partner",
            "investing partner",
            "led financing",
            "board observer",
        )
    ):
        return "Venture / financing role"
    if any(
        k in r
        for k in (
            "board chair",
            "interim board chair",
            "board member",
            "director since",
            "board appointment",
            "committee member",
        )
    ):
        return "ERA board / chair role"
    if any(
        k in r
        for k in ("appoints era", "appointed chief", "deputy minister", "government")
    ):
        return "Government / appointment"
    if any(
        k in r
        for k in (
            "senior executive",
            "president",
            "chief executive",
            "head of carbon",
            "fellow",
            "responsible officer",
        )
    ):
        return "Employment / executive tenure"
    if "own companies" in r or "program-management" in r:
        return "Management-owned company fees"
    if "lobbyist" in r:
        return "Lobbyist registration"
    if "competition coordination" in r or "crin" in r:
        return "CRIN commercial / board link"
    if "no match" in r or "intersection" in r:
        return "Database intersection (no hit)"
    if "award date" in r or "timing" in r:
        return "Decision-date confirmation"
    return "Other documented link"


def part6() -> None:
    edges_path = ROOT / "research/era-network/era-network-edges.csv"
    rows = list(csv.DictReader(edges_path.open(encoding="utf-8")))
    cats = Counter(edge_category(r["relationship"]) for r in rows)
    ordered = sorted(cats.items(), key=lambda x: x[1], reverse=True)
    labels = [k for k, _ in ordered]
    vals = [v for _, v in ordered]

    p6 = ROOT / "content/series/the-tier-files/part-6-the-small-world"
    fig, ax = plt.subplots(figsize=(12, 6.2))
    style_ax(ax, "44 sourced edges, by relationship type")
    y = np.arange(len(labels))
    colors = [
        ACCENT if i == 0 else (LIGHT if i > 4 else "#A0522D") for i in range(len(labels))
    ]
    ax.barh(y, vals, color=colors, height=0.65)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Number of edges")
    ax.set_xlim(0, max(vals) * 1.18)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for yi, v in zip(y, vals):
        ax.text(v + 0.25, yi, str(v), va="center", fontsize=10, color=INK, fontweight="bold")
    save(fig, p6 / "p6-edge-types.png")

    people, orgs = set(), set()
    for r in rows:
        for col in ("node_a", "node_b"):
            t = (r.get(f"{col}_type") or "").lower()
            n = r[col].strip()
            if "person" in t:
                people.add(n.split(",")[0].strip())
            else:
                orgs.add(n)

    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_title(
        "The pipeline: funded ecosystem to the boardroom",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color=INK,
        pad=8,
    )

    def box(x, y, w, h, title, sub, face):
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="square,pad=0",
                linewidth=1.2,
                edgecolor=ACCENT,
                facecolor=face,
            )
        )
        ax.text(
            x + w / 2,
            y + h * 0.62,
            title,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=INK,
        )
        ax.text(
            x + w / 2,
            y + h * 0.28,
            sub,
            ha="center",
            va="center",
            fontsize=10,
            color=MUTED,
        )

    box(
        0.4,
        2.0,
        3.2,
        2.2,
        "Builders / funders",
        "funded cos · VC portfolios\nemployers · partners",
        "#FFFFFF",
    )
    box(
        4.4,
        2.0,
        3.2,
        2.2,
        "People in the file",
        f"{len(people)} named individuals\nin the edge list",
        WASH,
    )
    box(
        8.4,
        2.0,
        3.2,
        2.2,
        "ERA board",
        "directors · chairs\nretrospective & concurrent",
        "#FFFFFF",
    )

    for x0, x1 in ((3.6, 4.4), (7.6, 8.4)):
        ax.annotate(
            "",
            xy=(x1, 3.1),
            xytext=(x0, 3.1),
            arrowprops=dict(arrowstyle="->", color=ACCENT, lw=2.0),
        )

    ax.add_patch(
        Rectangle((0.4, 0.35), 11.2, 1.2, facecolor="#FFFFFF", edgecolor=GRID, linewidth=1)
    )
    ax.text(2.2, 0.95, f"{len(rows)} edges", ha="center", fontsize=16, fontweight="bold", color=ACCENT)
    ax.text(2.2, 0.55, "sourced links", ha="center", fontsize=9, color=MUTED)
    ax.text(6.0, 0.95, f"{len(people)} people", ha="center", fontsize=16, fontweight="bold", color=ACCENT)
    ax.text(6.0, 0.55, "in the map", ha="center", fontsize=9, color=MUTED)
    ax.text(9.8, 0.95, f"{len(orgs)} orgs", ha="center", fontsize=16, fontweight="bold", color=ACCENT)
    ax.text(9.8, 0.55, "companies & agencies", ha="center", fontsize=9, color=MUTED)
    fig.text(0.01, 0.02, SOURCE, fontsize=8, color=MUTED, alpha=0.85)
    out = p6 / "p6-pipeline.png"
    fig.savefig(out, dpi=160, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", out.relative_to(ROOT))


def part7_cover() -> None:
    p7 = ROOT / "content/series/the-tier-files/part-7-the-companies-the-board-pays-itself"
    chart = Image.open(p7 / "p7-two-eras.png").convert("RGB")
    W, H = 1600, 1000
    cover = Image.new("RGB", (W, H), "#F3F3F2")
    pad = 56
    band_h = 200
    area_w, area_h = W - 2 * pad, H - band_h - pad - 24
    sw, sh = chart.size
    scale = min(area_w / sw, area_h / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = chart.resize((nw, nh), Image.Resampling.LANCZOS)
    panel = Image.new("RGB", (area_w, area_h), "#FFFFFF")
    panel.paste(resized, ((area_w - nw) // 2, (area_h - nh) // 2))
    cover.paste(panel, (pad, pad))
    d = ImageDraw.Draw(cover)
    d.rectangle([0, 0, 8, H], fill=ACCENT)
    d.rectangle([0, H - band_h, W, H], fill="#FFFFFF")
    d.line([(pad, H - band_h), (W - pad, H - band_h)], fill=GRID, width=2)
    try:
        fk = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 26)
        ft = ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", 40)
        fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
    except OSError:
        fk = ft = fs = ImageFont.load_default()
    y0 = H - band_h + 28
    d.text((pad + 6, y0), "THE TIER FILES  ·  PART 7", fill=ACCENT, font=fk)
    d.text((pad + 6, y0 + 42), "The Companies the Board Pays Itself", fill=INK, font=ft)
    d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill=MUTED, font=fs)
    out = p7 / "cover.png"
    cover.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(ROOT))


def what_era_announced() -> None:
    wea = ROOT / "content/essays/what-era-announced"
    proj = list(
        csv.DictReader((ROOT / "research/era-network/era-projects-database.csv").open(encoding="utf-8"))
    )
    status_order = [
        "Completed",
        "Active",
        "Contribution Agreement",
        "Never initiated",
        "Cancelled",
        "Terminated",
    ]
    sc = Counter(r["status"] for r in proj)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    style_ax(ax, "469 project pages: one in four is already dead")
    left = 0
    palette = {
        "Completed": "#5C4033",
        "Active": ACCENT,
        "Contribution Agreement": "#A0522D",
        "Never initiated": "#B0A89E",
        "Cancelled": "#8A8078",
        "Terminated": "#6B6560",
    }
    for st in status_order:
        v = sc[st]
        ax.barh(0, v, left=left, height=0.55, color=palette[st], edgecolor=BG, linewidth=1)
        if v >= 30:
            tc = "#FFFFFF" if st in ("Completed", "Active", "Contribution Agreement") else INK
            ax.text(
                left + v / 2,
                0,
                f"{st}\n{v}",
                ha="center",
                va="center",
                fontsize=9,
                color=tc,
                fontweight="bold",
            )
        left += v
    ax.set_xlim(0, 469)
    ax.set_yticks([])
    ax.set_xlabel("Projects in ERA WordPress database")
    handles = [plt.Rectangle((0, 0), 1, 1, color=palette[s]) for s in status_order]
    ax.legend(
        handles,
        [f"{s} ({sc[s]})" for s in status_order],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.18),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    ax.annotate(
        "116 dead (24.7%)",
        xy=(469 - 58, 0.35),
        xytext=(360, 0.85),
        fontsize=11,
        fontweight="bold",
        color=ACCENT,
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.3),
    )
    save(fig, wea / "wea-status-mix.png")

    fig, ax = plt.subplots(figsize=(12, 5.2))
    style_ax(ax, "Agreements cancelled or terminated: $179M in four years")
    years = ["FY2022", "FY2023", "FY2024", "FY2025"]
    canc = [19.9, 22.6, 53.8, 82.7]
    cols = [LIGHT, LIGHT, "#A0522D", ACCENT]
    ax.bar(years, canc, color=cols, width=0.58)
    ax.set_ylabel("$ millions")
    ax.set_ylim(0, 100)
    ax.yaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for x_, y_ in zip(years, canc):
        ax.text(
            x_,
            y_ + 2.5,
            f"${y_:.1f}M",
            ha="center",
            fontsize=10,
            color=INK,
            fontweight="bold",
        )
    ax.axhline(38.0, color=MUTED, linestyle="--", linewidth=1.0, alpha=0.7)
    ax.text(
        0.02,
        40.5,
        "Database Terminated rows still list ~$38M (Cancelled/Never initiated blanked to $0)",
        transform=ax.get_yaxis_transform(),
        fontsize=8.5,
        color=MUTED,
    )
    save(fig, wea / "wea-dead-dollars.png")


def missing_year() -> None:
    my = ROOT / "content/essays/the-missing-year"
    fig, ax = plt.subplots(figsize=(12, 4.2))
    ax.set_xlim(2009.5, 2026.5)
    ax.set_ylim(0, 3)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_title(
        "Fifteen years of statements on the shelf — except fiscal 2015",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color=INK,
        pad=10,
    )
    ax.plot([2010, 2025], [1.5, 1.5], color=GRID, lw=2)
    years_ok = list(range(2010, 2015)) + list(range(2016, 2026))
    for y in years_ok:
        ax.plot(y, 1.5, "o", color=ACCENT, markersize=7)
        if y in (2010, 2014, 2016, 2020, 2025):
            ax.text(y, 1.15, str(y), ha="center", fontsize=9, color=MUTED)
    ax.plot(2015, 1.5, "o", color=BG, markersize=14, markeredgecolor=ACCENT, markeredgewidth=2.5)
    ax.plot(2015, 1.5, "x", color=ACCENT, markersize=10, markeredgewidth=2)
    ax.annotate(
        "FY2015\nstatements\nmissing",
        xy=(2015, 1.65),
        xytext=(2015, 2.55),
        ha="center",
        fontsize=11,
        fontweight="bold",
        color=ACCENT,
        arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.4),
    )
    ax.text(2012, 0.45, "CCEMC era", ha="center", fontsize=10, color=MUTED)
    ax.text(2021, 0.45, "ERA era (statements published)", ha="center", fontsize=10, color=MUTED)
    fig.text(0.01, 0.04, SOURCE, fontsize=8, color=MUTED, alpha=0.85)
    out = my / "my-gap-timeline.png"
    fig.savefig(out, dpi=160, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", out.relative_to(ROOT))


def nineteen_recs() -> None:
    ag = ROOT / "content/essays/nineteen-recommendations"
    ag_rows = list(
        csv.DictReader((ROOT / "research/essays-next/ag-epa-recommendations.csv").open(encoding="utf-8"))
    )
    outstanding_statuses = {
        "Not Ready for Assessment": 0,
        "Ready for Assessment": 0,
        "Not Implemented": 0,
    }
    closed_impl = 0
    for r in ag_rows:
        st = r["status"]
        if st in outstanding_statuses:
            outstanding_statuses[st] += 1
        elif "Implemented" in st or "Closed" in st:
            closed_impl += 1

    fig, ax = plt.subplots(figsize=(12, 5.0))
    style_ax(ax, "EPA outstanding AG recommendations: 19 down to 13")
    cats = [
        "Outstanding\n(Dec 2023)",
        "Outstanding\n(Dec 2025)",
        "Not Ready\n(current)",
        "Ready for\nassessment",
        "Not\nImplemented",
        "Closed /\nimplemented\nin file",
    ]
    vals2 = [
        19,
        13,
        outstanding_statuses["Not Ready for Assessment"],
        outstanding_statuses["Ready for Assessment"],
        outstanding_statuses["Not Implemented"],
        closed_impl,
    ]
    y = np.arange(len(cats))
    bar_cols = [LIGHT, ACCENT, "#A0522D", "#A0522D", "#5C4033", MUTED]
    ax.barh(y, vals2, color=bar_cols, height=0.6)
    ax.set_yticks(y)
    ax.set_yticklabels(cats, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel("Recommendations")
    ax.set_xlim(0, 22)
    ax.xaxis.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for yi, v in zip(y, vals2):
        ax.text(v + 0.35, yi, str(v), va="center", fontsize=11, fontweight="bold", color=INK)
    save(fig, ag / "ag-outstanding.png")


def part5_layers() -> None:
    p5 = ROOT / "content/series/the-tier-files/part-5-paid-in-alberta-claimed-everywhere"
    fig, ax = plt.subplots(figsize=(12, 5.8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_title(
        "Who gets to claim the tonne: three paper objects",
        loc="left",
        fontsize=14,
        fontweight="bold",
        color=INK,
        pad=8,
    )
    layers = [
        (
            6.2,
            ACCENT,
            "1  ERA / provincial program claim",
            "Portfolio KPI language: funded reductions\nbooked toward Alberta climate results",
        ),
        (
            3.9,
            "#A0522D",
            "2  Alberta Emission Offset Registry",
            "Verified AEOR serials — TIER compliance\ninstruments inside Alberta",
        ),
        (
            1.6,
            "#5C4033",
            "3  BC biomethane environmental attributes",
            "FortisBC BPAs / GGRR — reductions booked\ninto British Columbia climate machinery",
        ),
    ]
    for y, face, title, sub in layers:
        ax.add_patch(
            FancyBboxPatch(
                (0.5, y),
                9.0,
                1.9,
                boxstyle="square,pad=0",
                linewidth=1.4,
                edgecolor=face,
                facecolor="#FFFFFF",
            )
        )
        ax.add_patch(Rectangle((0.5, y), 0.18, 1.9, facecolor=face, edgecolor=face))
        ax.text(1.0, y + 1.25, title, fontsize=13, fontweight="bold", color=face, va="center")
        ax.text(1.0, y + 0.55, sub, fontsize=10, color=MUTED, va="center", linespacing=1.35)
    ax.text(
        5.0,
        0.45,
        "One physical reduction · concurrent claim systems · no public mass balance between ledgers",
        ha="center",
        fontsize=10,
        color=INK,
        style="italic",
    )
    fig.text(0.01, 0.02, SOURCE, fontsize=8, color=MUTED, alpha=0.85)
    out = p5 / "p5-claim-layers.png"
    fig.savefig(out, dpi=160, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    part6()
    part7_cover()
    what_era_announced()
    missing_year()
    nineteen_recs()
    part5_layers()
    print("DONE")
