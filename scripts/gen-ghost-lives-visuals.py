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
    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.2)
    ax.axis("off")
    ax.set_title("Five claims one reduction can carry", loc="left", fontsize=14, fontweight="bold", color=INK, pad=8)

    core = (3.6, 2.95, 2.8, 1.4)  # x, y, w, h
    claims = [
        (0.25, 5.35, 2.9, 1.4, "1  Voluntary premium\n$7-$8.66 / GJ"),
        (3.55, 5.35, 2.9, 1.4, "2  Mandatory blend\n3-3.5% on every bill"),
        (6.85, 5.35, 2.9, 1.4, "3  Carbon-tax refund\nprovincial fiscal ghost"),
        (1.4, 0.55, 2.9, 1.4, "4  CFR credit\nsold to liquid-fuel suppliers"),
        (5.7, 0.55, 2.9, 1.4, "5  BC LCFS credit\nRNG in CNG (often BC-based)"),
    ]

    cx = core[0] + core[2] / 2
    cy = core[1] + core[3] / 2

    def stop_before(src, dst_box, margin=0.30):
        dx0, dy0, dw, dh = dst_box[:4]
        tx, ty = dx0 + dw / 2, dy0 + dh / 2
        vx, vy = tx - src[0], ty - src[1]
        length = (vx * vx + vy * vy) ** 0.5
        ux, uy = vx / length, vy / length
        t_candidates = []
        if abs(ux) > 1e-9:
            for edge_x in (dx0, dx0 + dw):
                t = (edge_x - src[0]) / ux
                if t > 0:
                    y = src[1] + t * uy
                    if dy0 - 1e-9 <= y <= dy0 + dh + 1e-9:
                        t_candidates.append(t)
        if abs(uy) > 1e-9:
            for edge_y in (dy0, dy0 + dh):
                t = (edge_y - src[1]) / uy
                if t > 0:
                    x = src[0] + t * ux
                    if dx0 - 1e-9 <= x <= dx0 + dw + 1e-9:
                        t_candidates.append(t)
        if not t_candidates:
            return tx, ty
        t_hit = min(t_candidates)
        t_stop = max(0.05, t_hit - margin)
        return src[0] + t_stop * ux, src[1] + t_stop * uy

    def leave_core(dst, margin=0.08):
        vx, vy = dst[0] - cx, dst[1] - cy
        length = (vx * vx + vy * vy) ** 0.5
        ux, uy = vx / length, vy / length
        x0, y0, w, h = core
        t_candidates = []
        if abs(ux) > 1e-9:
            for edge_x in (x0, x0 + w):
                t = (edge_x - cx) / ux
                if t > 0:
                    y = cy + t * uy
                    if y0 - 1e-9 <= y <= y0 + h + 1e-9:
                        t_candidates.append(t)
        if abs(uy) > 1e-9:
            for edge_y in (y0, y0 + h):
                t = (edge_y - cy) / uy
                if t > 0:
                    x = cx + t * ux
                    if x0 - 1e-9 <= x <= x0 + w + 1e-9:
                        t_candidates.append(t)
        t_hit = min(t_candidates) if t_candidates else 0.7
        t_start = t_hit + margin
        return cx + t_start * ux, cy + t_start * uy

    for box in claims:
        end = stop_before((cx, cy), box, margin=0.32)
        start = leave_core(end, margin=0.06)
        ax.add_patch(
            FancyArrowPatch(
                start,
                end,
                arrowstyle="-|>",
                mutation_scale=10,
                color=SECONDARY,
                lw=1.15,
                connectionstyle="arc3,rad=0.0",
                shrinkA=0,
                shrinkB=0,
                zorder=1,
            )
        )

    ax.add_patch(
        FancyBboxPatch(
            (core[0], core[1]),
            core[2],
            core[3],
            boxstyle="square,pad=0",
            linewidth=2,
            edgecolor=HIGHLIGHT,
            facecolor="#FFF5F5",
            zorder=5,
        )
    )
    ax.text(cx, cy, "ONE METHANE\nREDUCTION", ha="center", va="center", fontsize=11, fontweight="bold", color=HIGHLIGHT, zorder=6)

    for x, y, w, h, text in claims:
        ax.add_patch(
            FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="square,pad=0",
                linewidth=1.2,
                edgecolor=GRID,
                facecolor="#F3F3F2",
                zorder=5,
            )
        )
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9, color=INK, linespacing=1.35, zorder=6)

    ax.text(
        5,
        0.12,
        "Architecture from FEI filings in BCUC G-137-25 / G-77-24. Not every GJ carries every claim.",
        ha="center",
        fontsize=8,
        color=MUTED,
        zorder=6,
    )
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
    ax.text(
        6,
        1.25,
        "FEI Stage 2 IR: majority of expected contracted RNG volume is from outside BC.\nBCUC Phase 1/2 accepted notional delivery for GGRR purposes if attribute tracking is robust.",
        ha="center",
        va="center",
        fontsize=9.5,
        color=INK,
        linespacing=1.4,
    )
    save(fig, P1 / "p1-displacement.png")


def ghost_lives_stack():
    fig, ax = plt.subplots(figsize=(10.5, 7.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title("Ghost lives on one physical reduction", loc="left", fontsize=14, fontweight="bold", color=INK)

    rows = [
        (9.2, HIGHLIGHT, "Physical event", "Methane captured at digester; one atmospheric job"),
        (7.7, SECONDARY, "Life 2 · Alberta", "Program / portfolio claim (and maybe an AEOR serial)"),
        (6.2, SECONDARY, "Life 3 · BC utility", "GGRR attribute sold; bill says renewable"),
        (4.7, SECONDARY, "Life 3b · Tax", "Provincial carbon-tax refund on the volume"),
        (3.2, SECONDARY, "Life 4 · CFR", "Federal credit sold into gasoline/diesel compliance"),
        (1.7, SECONDARY, "Life 5 · LCFS", "BC transportation credit if pathway is eligible"),
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
    splash = P2 / "comic-00-splash.png"
    if splash.exists():
        make_cover(splash, SERIES / "cover.png", 0, "Ghost Lives")
        img = Image.open(SERIES / "cover.png")
        d = ImageDraw.Draw(img)
        fk, ft, fs = fonts((26, 52, 20))
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
