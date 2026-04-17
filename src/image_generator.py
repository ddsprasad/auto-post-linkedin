"""
Infographic image generator for LinkedIn posts.
Creates clean, professional 1200x628 PNG images using Pillow.
"""

import io
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

IMG_W, IMG_H = 1200, 628
HEADER_H = 72
FOOTER_H = 52
PAD = 50

# Color scheme per topic
SCHEMES = {
    "gen_ai":     {"dark": "#1E3A8A", "light": "#EFF6FF", "mid": "#DBEAFE"},
    "databricks": {"dark": "#991B1B", "light": "#FEF2F2", "mid": "#FEE2E2"},
    "sql_server": {"dark": "#0F766E", "light": "#F0FDFA", "mid": "#CCFBF1"},
}
TEXT_COL = "#1E293B"
MUTED_COL = "#475569"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    paths = (
        [
            "C:/Windows/Fonts/arialbd.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "C:/Windows/Fonts/arial.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def render_infographic(
    topic_key: str,
    topic_name: str,
    post_number: int,
    title: str,
    points: list[str],
) -> bytes:
    """
    Render a professional infographic image for a LinkedIn post.
    Returns PNG bytes.
    """
    scheme = SCHEMES.get(topic_key, SCHEMES["gen_ai"])
    dark_rgb = _hex_to_rgb(scheme["dark"])
    light_rgb = _hex_to_rgb(scheme["light"])
    mid_rgb = _hex_to_rgb(scheme["mid"])

    img = Image.new("RGB", (IMG_W, IMG_H), light_rgb)
    d = ImageDraw.Draw(img)

    # ── Header band ──────────────────────────────────────
    d.rectangle([0, 0, IMG_W, HEADER_H], fill=dark_rgb)

    topic_display = topic_name.upper()
    d.text((PAD, 20), topic_display, fill="white", font=_font(28, bold=True))

    # ── Left accent bar ───────────────────────────────────
    d.rectangle([0, HEADER_H, 6, IMG_H - FOOTER_H], fill=dark_rgb)

    # ── Title ─────────────────────────────────────────────
    y = HEADER_H + 28
    title_font = _font(38, bold=True)
    for line in textwrap.wrap(title, width=40)[:2]:
        d.text((PAD + 16, y), line, fill=TEXT_COL, font=title_font)
        y += 50

    # ── Divider ───────────────────────────────────────────
    y += 8
    d.rectangle([PAD + 16, y, IMG_W - PAD, y + 2], fill=mid_rgb)
    y += 18

    # ── Key points ────────────────────────────────────────
    pt_font = _font(22)
    num_font = _font(15, bold=True)

    for i, pt in enumerate(points[:5]):
        if y > IMG_H - FOOTER_H - 38:
            break

        # Numbered circle bullet
        cx, cy = PAD + 28, y + 16
        r = 15
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=dark_rgb)
        num_str = str(i + 1)
        nx = cx - 5 if len(num_str) == 1 else cx - 8
        d.text((nx, cy - 11), num_str, fill="white", font=num_font)

        # Point text
        pt_lines = textwrap.wrap(pt, width=74)[:2]
        for j, line in enumerate(pt_lines):
            d.text((PAD + 58, y + j * 27), line, fill=TEXT_COL, font=pt_font)

        line_count = len(pt_lines)
        y += max(44, line_count * 27 + 14)

    # ── Footer band ───────────────────────────────────────
    d.rectangle([0, IMG_H - FOOTER_H, IMG_W, IMG_H], fill=dark_rgb)
    footer_txt = "Follow for daily posts on AI, Databricks & SQL Server"
    d.text((PAD, IMG_H - FOOTER_H + 14), footer_txt, fill="white", font=_font(20))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()
