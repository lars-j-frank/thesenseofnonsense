"""
Render LinkedIn-ready PNGs for Lars J. Frank.

Downloads OFL variable fonts once into brand/linkedin/fonts/, then paints:
  - avatar-lf-800.png / avatar-sn-800.png (800×800)
  - banner-primary-1584x396.png
  - banner-ledger-1584x396.png

Run from repo root:
  py -3 brand/linkedin/scripts/render-linkedin-assets.py
"""

from __future__ import annotations

import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONTS = ROOT / "fonts"

RED = (222, 0, 0)  # #DE0000
GREY = (60, 61, 60)  # #3C3D3C
MANHATTAN = (82, 82, 82)  # #525252
TITANIUM = (139, 135, 131)  # #8B8783
BORDER = (214, 212, 209)  # #D6D4D1
WHITE = (255, 255, 255)

# LinkedIn profile photo overlaps bottom-left of the banner (~300px circle).
# Keep all readable type to the right of this inset.
BANNER_TEXT_X = 460

FONT_URLS = {
    "LibreFranklin.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/librefranklin/LibreFranklin%5Bwght%5D.ttf",
    "SourceSerif4.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourceserif4/SourceSerif4%5Bopsz%2Cwght%5D.ttf",
    "SourceSerif4-Italic.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/sourceserif4/SourceSerif4-Italic%5Bopsz%2Cwght%5D.ttf",
}


def ensure_fonts() -> None:
    FONTS.mkdir(parents=True, exist_ok=True)
    for name, url in FONT_URLS.items():
        dest = FONTS / name
        if dest.exists() and dest.stat().st_size > 1000:
            continue
        print(f"Downloading {name}")
        with urllib.request.urlopen(url, timeout=60) as resp:
            dest.write_bytes(resp.read())


def load_font(path: Path, size: int, variation: str | None = None) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(path), size=size)
    if variation:
        try:
            font.set_variation_by_name(variation)
        except Exception:
            # Source Serif opsz+wght: name may still work; else leave default
            pass
    return font


def render_avatar(initials: str, out: Path) -> None:
    size = 800
    img = Image.new("RGB", (size, size), GREY)
    draw = ImageDraw.Draw(img)
    spine = 72
    draw.rectangle([0, 0, spine, size], fill=RED)
    font = load_font(FONTS / "LibreFranklin.ttf", 260, "Bold")
    bbox = draw.textbbox((0, 0), initials, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = spine + (size - spine - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] - 8
    draw.text((x, y), initials, font=font, fill=WHITE)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.name}")


def render_banner_primary(out: Path) -> None:
    w, h = 1584, 396
    x = BANNER_TEXT_X
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 18, h], fill=RED)
    draw.line([(18, 0), (18, h)], fill=BORDER, width=1)

    # Soft ruling in the avatar zone only (may be covered)
    for y, x2 in ((220, 380), (256, 340), (292, 300), (328, 260)):
        draw.line([(48, y), (x2, y)], fill=BORDER, width=1)

    name_font = load_font(FONTS / "SourceSerif4.ttf", 58, "SemiBold")
    pub_font = load_font(FONTS / "LibreFranklin.ttf", 22, "Bold")
    tag_font = load_font(FONTS / "SourceSerif4-Italic.ttf", 24, "Regular")

    draw.text((x, 100), "Lars J. Frank", font=name_font, fill=GREY)
    draw.text((x, 172), "THE SENSE OF NONSENSE", font=pub_font, fill=MANHATTAN)
    draw.line([(x, 212), (x + 240, 212)], fill=RED, width=2)
    draw.text(
        (x, 236),
        "Stories and analysis from within the nonsense",
        font=tag_font,
        fill=TITANIUM,
    )

    for i, y in enumerate(range(90, 307, 36)):
        x2 = 1512 if i < 6 else 1440
        draw.line([(1180, y), (x2, y)], fill=BORDER, width=1)
    draw.rectangle([1180, 90, 1188, 306], fill=RED)

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.name}")


def render_banner_ledger(out: Path) -> None:
    w, h = 1584, 396
    x = BANNER_TEXT_X
    img = Image.new("RGB", (w, h), GREY)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, 18, h], fill=RED)

    for y, x2 in ((220, 380), (256, 340), (292, 300), (328, 260)):
        draw.line([(48, y), (x2, y)], fill=(100, 100, 98), width=1)

    tag_font = load_font(FONTS / "SourceSerif4.ttf", 38, "SemiBold")
    meta_font = load_font(FONTS / "LibreFranklin.ttf", 18, "Bold")

    draw.text(
        (x, 125),
        "Stories and analysis from within the nonsense",
        font=tag_font,
        fill=WHITE,
    )
    draw.text(
        (x, 190),
        "LARS J. FRANK  ·  THE TIER FILES  ·  THESENSEOFNONSENSE.COM",
        font=meta_font,
        fill=TITANIUM,
    )
    for y, x2 in ((280, 1180), (308, 1040), (336, 1100)):
        draw.line([(x, y), (x2, y)], fill=(100, 100, 98), width=1)

    img.save(out, "PNG", optimize=True)
    print(f"wrote {out.name}")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    ensure_fonts()
    render_avatar("LF", ASSETS / "avatar-lf-800.png")
    render_avatar("SN", ASSETS / "avatar-sn-800.png")
    render_banner_primary(ASSETS / "banner-primary-1584x396.png")
    render_banner_ledger(ASSETS / "banner-ledger-1584x396.png")
    # Remove font probe if present
    probe = ASSETS / "_font-test.png"
    if probe.exists():
        probe.unlink()
    print("done")


if __name__ == "__main__":
    main()
