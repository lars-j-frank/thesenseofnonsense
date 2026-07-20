"""Charts and covers for Ghost Lives series."""
from __future__ import annotations

import shutil
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SERIES = ROOT / "content" / "series" / "ghost-lives"
P1 = SERIES / "part-1-what-the-premium-buys"
P2 = SERIES / "part-2-where-stacking-ends"
ASSETS = Path(r"C:\Users\jcran\.cursor\projects\c-Users-jcran-Documents-thesenseofnonsense\assets")

BG = "#FFFFFF"
WASH = "#F3F3F2"
INK = "#3C3D3C"
MUTED = "#8B8783"
HIGHLIGHT = "#DE0000"
SECONDARY = "#525252"
GRID = "#D6D4D1"
GHOST = "#C5C3C0"
SOURCE = "Source: BCUC / FEI filings summarised in Ghost Lives. thesenseofnonsense.com"

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 13,
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Helvetica"],
})


def save(fig, path: Path):
    fig.patch.set_facecolor(BG)
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.text(0.01, 0.012, SOURCE, fontsize=8, color=MUTED)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=180, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print("wrote", path.relative_to(ROOT))


def fonts(sizes=(26, 44, 20)):
    try:
        return (
            ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", sizes[0]),
            ImageFont.truetype("C:/Windows/Fonts/georgia.ttf", sizes[1]),
            ImageFont.truetype("C:/Windows/Fonts/arial.ttf", sizes[2]),
        )
    except OSError:
        f = ImageFont.load_default()
        return f, f, f


def make_cover(panel: Path, out: Path, part: int, title: str):
    img = Image.open(panel).convert("RGB")
    W, H = 1600, 1000
    cover = Image.new("RGB", (W, H), WASH)
    pad, band_h = 56, 200
    area_w, area_h = W - 2 * pad, H - band_h - pad - 24
    sw, sh = img.size
    scale = min(area_w / sw, area_h / sh)
    nw, nh = int(sw * scale), int(sh * scale)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    panel_img = Image.new("RGB", (area_w, area_h), BG)
    panel_img.paste(resized, ((area_w - nw) // 2, (area_h - nh) // 2))
    cover.paste(panel_img, (pad, pad))
    d = ImageDraw.Draw(cover)
    d.rectangle([0, 0, 8, H], fill=HIGHLIGHT)
    d.rectangle([0, H - band_h, W, H], fill=BG)
    d.line([(pad, H - band_h), (W - pad, H - band_h)], fill=GRID, width=2)
    fk, ft, fs = fonts()
    y0 = H - band_h + 28
    d.text((pad + 6, y0), f"GHOST LIVES  ·  PART {part}", fill=HIGHLIGHT, font=fk)
    d.text((pad + 6, y0 + 42), title, fill=INK, font=ft)
    d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill=MUTED, font=fs)
    cover.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(ROOT))


def five_claims():
    fig, ax = plt.subplots(figsize=(10.5, 6.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")
    ax.set_title("Five claims one reduction can carry", loc="left", fontsize=14, fontweight="bold", color=INK, pad=8)

    # Core
    ax.add_patch(FancyBboxPatch((3.6, 2.9), 2.8, 1.4, boxstyle="square,pad=0", linewidth=2, edgecolor=HIGHLIGHT, facecolor="#FFF5F5"))
    ax.text(5, 3.6, "ONE METHANE\nREDUCTION", ha="center", va="center", fontsize=11, fontweight="bold", color=HIGHLIGHT)

    claims = [
        (0.3, 5.2, "1  Voluntary premium\n$7–$8.66 / GJ"),
        (3.6, 5.2, "2  Mandatory blend\n3% on every bill"),
        (6.9, 5.2, "3  Carbon-tax refund\nprovincial fiscal ghost"),
        (1.5, 0.6, "4  CFR credit\nsold to liquid-fuel suppliers"),
        (5.5, 0.6, "5  BC LCFS credit\nRNG in CNG vehicles"),
    ]
    for x, y, text in claims:
        ax.add_patch(FancyBboxPatch((x, y), 2.8, 1.35, boxstyle="square,pad=0", linewidth=1, edgecolor=GRID, facecolor=WASH))
        ax.text(x + 1.4, y + 0.67, text, ha="center", va="center", fontsize=9, color=INK, linespacing=1.35)

    for x, y, _ in claims:
        ax.add_patch(FancyArrowPatch((5, 3.6), (x + 1.4, y + 0.7), arrowstyle="-|>", mutation_scale=12, color=SECONDARY, lw=1.2, connectionstyle="arc3,rad=0.05"))

    ax.text(5, 0.15, "Architecture from FEI filings in BCUC G-137-25 / G-77-24. Not every GJ carries every claim.", ha="center", fontsize=8, color=MUTED)
    save(fig, P1 / "p1-five-claims.png")


def displacement():
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis("off")
    ax.set_title("Displacement delivery: molecules stay, attributes travel", loc="left", fontsize=14, fontweight="bold", color=INK)

    boxes = [
        (0.3, 2.8, 3.0, 1.5, "Out-of-province\nbiomethane injected\nlocally", WASH),
        (4.5, 2.8, 3.0, 1.5, "Nearby customers\nburn those molecules\nas ordinary gas", WASH),
        (8.7, 2.8, 3.0, 1.5, "At hub: attributes\n+ conventional gas\n= RNG for FEI", "#FFF5F5"),
    ]
    for x, y, w, h, text, face in boxes:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", linewidth=1.5, edgecolor=HIGHLIGHT if face != WASH else GRID, facecolor=face))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10, color=INK, linespacing=1.35)

    ax.annotate("", xy=(4.4, 3.55), xytext=(3.4, 3.55), arrowprops=dict(arrowstyle="-|>", color=SECONDARY, lw=1.5))
    ax.annotate("", xy=(8.6, 3.55), xytext=(7.6, 3.55), arrowprops=dict(arrowstyle="-|>", color=HIGHLIGHT, lw=1.8))

    ax.add_patch(FancyBboxPatch((0.3, 0.5), 11.4, 1.5, boxstyle="square,pad=0", linewidth=1, edgecolor=GRID, facecolor=WASH))
    ax.text(6, 1.25, "FEI Stage 2 record: over 70% of contracted RNG supply is from outside BC.\nBCUC Phase 1/2 accepted notional delivery for GGRR purposes if attribute tracking is robust.", ha="center", va="center", fontsize=9.5, color=INK, linespacing=1.4)
    save(fig, P1 / "p1-displacement.png")


def ghost_lives_stack():
    fig, ax = plt.subplots(figsize=(10.5, 7.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title("Ghost lives on one physical reduction", loc="left", fontsize=14, fontweight="bold", color=INK)

    rows = [
        (9.2, HIGHLIGHT, "Physical event", "Methane captured at digester — one atmospheric job"),
        (7.7, SECONDARY, "Life 2 · Alberta", "Program / portfolio claim (and maybe an AEOR serial)"),
        (6.2, SECONDARY, "Life 3 · BC utility", "GGRR attribute sold; bill says renewable"),
        (4.7, SECONDARY, "Life 3b · Tax", "Provincial carbon-tax refund on the volume"),
        (3.2, SECONDARY, "Life 4 · CFR", "Federal credit sold into gasoline/diesel compliance"),
        (1.7, SECONDARY, "Life 5 · LCFS", "BC transportation credit if burned in CNG"),
    ]
    for y, edge, label, desc in rows:
        face = "#FFF5F5" if edge == HIGHLIGHT else WASH
        ax.add_patch(FancyBboxPatch((0.4, y), 9.2, 1.2, boxstyle="square,pad=0", linewidth=1.5 if edge == HIGHLIGHT else 1, edgecolor=edge, facecolor=face))
        ax.text(0.7, y + 0.6, label, ha="left", va="center", fontsize=10, fontweight="bold", color=HIGHLIGHT if edge == HIGHLIGHT else INK)
        ax.text(9.3, y + 0.6, desc, ha="right", va="center", fontsize=9.5, color=INK)

    ax.text(5, 0.6, "Permission structure from public filings. Not every tonne carries every life.", ha="center", fontsize=8.5, color=MUTED)
    save(fig, P2 / "p2-ghost-stack.png")


def copy_comics():
    mapping = [
        ("ghost-comic-00-splash.png", P2 / "comic-00-splash.png"),
        ("ghost-comic-01-lagoon.png", P2 / "comic-01-lagoon.png"),
        ("ghost-comic-02-digester.png", P2 / "comic-02-digester.png"),
        ("ghost-comic-03-alberta.png", P2 / "comic-03-alberta.png"),
        ("ghost-comic-04-displacement.png", P2 / "comic-04-displacement.png"),
        ("ghost-comic-05-ratepayer.png", P2 / "comic-05-ratepayer.png"),
        ("ghost-comic-06-cfr.png", P2 / "comic-06-cfr.png"),
        ("ghost-comic-07-finale.png", P2 / "comic-07-finale.png"),
        # Part 1 also gets splash + displacement + five-claims related stills
        ("ghost-comic-00-splash.png", P1 / "comic-splash.png"),
        ("ghost-comic-04-displacement.png", P1 / "comic-displacement.png"),
        ("ghost-comic-05-ratepayer.png", P1 / "comic-ratepayer.png"),
        ("ghost-comic-07-finale.png", P1 / "comic-finale.png"),
    ]
    for src_name, dest in mapping:
        src = ASSETS / src_name
        if not src.exists():
            print("MISSING", src)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print("copied", dest.relative_to(ROOT))


def main():
    five_claims()
    displacement()
    ghost_lives_stack()
    copy_comics()
    make_cover(P1 / "p1-five-claims.png", P1 / "cover.png", 1, "What the Premium Buys")
    make_cover(P2 / "comic-07-finale.png", P2 / "cover.png", 2, "Where Stacking Ends")
    # series cover from splash
    splash = P2 / "comic-00-splash.png"
    if splash.exists():
        make_cover(splash, SERIES / "cover.png", 0, "Ghost Lives")
        # fix series band label
        img = Image.open(SERIES / "cover.png")
        d = ImageDraw.Draw(img)
        fk, ft, fs = fonts((26, 52, 20))
        # repaint bottom band text cleaner for series
        W, H = img.size
        pad, band_h = 56, 200
        d.rectangle([0, H - band_h, W, H], fill=BG)
        d.line([(pad, H - band_h), (W - pad, H - band_h)], fill=GRID, width=2)
        d.rectangle([0, 0, 8, H], fill=HIGHLIGHT)
        y0 = H - band_h + 28
        d.text((pad + 6, y0), "SERIES", fill=HIGHLIGHT, font=fk)
        d.text((pad + 6, y0 + 42), "Ghost Lives", fill=INK, font=ft)
        d.text((pad + 6, H - 42), "thesenseofnonsense.com", fill=MUTED, font=fs)
        img.save(SERIES / "cover.png", "PNG", optimize=True)
        print("wrote series cover")


if __name__ == "__main__":
    main()
