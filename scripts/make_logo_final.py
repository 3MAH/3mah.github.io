"""The 3MAH logo (logo_final.pdf) with a transparent background.

The PDF is converted to SVG, its white page rectangle is removed, and the embedded
waves image (white background) gets a white-to-alpha treatment. Outputs:
  docs/assets/images/logo_3mah/3mah_logo.svg           vector ship + embedded waves
  docs/assets/images/logo_3mah/3mah_logo.png           512 px high, header logo
  docs/assets/images/logo_3mah/favicon.png             64 px square

    DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python scripts/make_logo_final.py

Needs `pdftocairo` (poppler), cairosvg, numpy and Pillow.
"""

import base64
import io
import re
import subprocess
import tempfile
from pathlib import Path

import cairosvg
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "docs" / "assets" / "images" / "logo_3mah"
SRC = IMG / "logo_final.pdf"


def white_to_alpha(im):
    rgba = np.asarray(im.convert("RGBA")).astype(float) / 255
    rgb, a0 = rgba[..., :3], rgba[..., 3]
    alpha = (1 - rgb).max(axis=2)
    safe = np.where(alpha > 0, alpha, 1)[..., None]
    rgb = np.clip(1 - (1 - rgb) / safe, 0, 1)
    alpha = np.where(alpha < 0.02, 0, alpha) * a0
    return Image.fromarray((np.dstack([rgb, alpha]) * 255).round().astype(np.uint8), "RGBA")


def transparent_image(match):
    data = base64.b64decode(match.group(2))
    buf = io.BytesIO()
    white_to_alpha(Image.open(io.BytesIO(data))).save(buf, "PNG")
    return f'{match.group(1)}data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"'


def main():
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "logo.svg"
        subprocess.run(["pdftocairo", "-svg", str(SRC), str(raw)], check=True)
        svg = raw.read_text()
    svg, n = re.subn(r'<rect [^>]*fill="rgb\(100%, 100%, 100%\)"[^>]*/>', "", svg)
    assert n == 1, f"expected one background rectangle, found {n}"
    # the image used as colour (not the one used as mask) is the waves render
    svg, n = re.subn(r'(<image id="source-6"[^>]*?(?:xlink:)?href=")data:image/[a-z]+;base64,([^"]+)"',
                     transparent_image, svg)
    assert n == 1, f"expected the waves image, found {n}"
    # crop to the drawing
    png = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), scale=4)))
    left, top, right, bottom = png.getchannel("A").getbbox()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    k = vb[2] / png.width
    x, y, w, h = vb[0] + left * k - 2, vb[1] + top * k - 2, (right - left) * k + 4, (bottom - top) * k + 4
    svg = re.sub(r'width="[^"]+" height="[^"]+" viewBox="[^"]+"',
                 f'width="{w:.2f}pt" height="{h:.2f}pt" viewBox="{x:.2f} {y:.2f} {w:.2f} {h:.2f}"', svg, count=1)
    (IMG / "3mah_logo.svg").write_text(svg, encoding="utf-8")
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(IMG / "3mah_logo.png"), output_height=512)
    big = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode(), output_height=256)))
    side = max(big.size)
    square = Image.new("RGBA", (side, side))
    square.paste(big, ((side - big.width) // 2, (side - big.height) // 2))
    square.resize((64, 64), Image.LANCZOS).save(IMG / "favicon.png")
    print("docs/assets/images/logo_3mah/3mah_logo.{svg,png}, favicon.png")


if __name__ == "__main__":
    main()
