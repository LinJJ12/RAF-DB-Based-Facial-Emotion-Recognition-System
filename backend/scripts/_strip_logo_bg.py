"""Extract rounded app icon from design PNG; transparent outside squircle."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
SRC_CANDIDATES = [
    ROOT / "docs" / "brand" / "logo-design-source.png",
    ROOT / "frontend" / "public" / "logo.png",
]
TARGETS = [
    ROOT / "frontend" / "public" / "logo.png",
    ROOT / "frontend" / "public" / "favicon.png",
    ROOT / "frontend" / "src" / "assets" / "brand" / "logo.png",
]


def find_source() -> Path:
    for p in SRC_CANDIDATES:
        if p.exists():
            return p
    raise FileNotFoundError("logo source not found")


def extract_icon(img: Image.Image) -> Image.Image:
    arr = np.array(img.convert("RGBA"), dtype=np.uint8)
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)

    # Canvas is near-white; icon plate is light cyan/blue (high B, not white)
    bright = (r + g + b) / 3.0
    sat = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
    canvas = (bright > 240) & (sat < 18)

    # Blue plate: cyan-ish, not the yellow face alone
    blue_plate = (~canvas) & (b > 180) & (g > 160) & (r < 220) & (b >= r - 5)

    ys, xs = np.where(blue_plate)
    if len(xs) < 1000:
        # fallback: any non-canvas
        ys, xs = np.where(~canvas)
    x0, x1 = int(xs.min()), int(xs.max())
    y0, y1 = int(ys.min()), int(ys.max())

    # Ignore bottom-right watermark strip on canvas (outside plate)
    # Tighten using blue_plate percentiles to avoid watermark outliers
    if blue_plate.any():
        ys_b, xs_b = np.where(blue_plate)
        x0 = int(np.percentile(xs_b, 0.2))
        x1 = int(np.percentile(xs_b, 99.8))
        y0 = int(np.percentile(ys_b, 0.2))
        y1 = int(np.percentile(ys_b, 99.8))

    pad = 2
    x0 = max(x0 - pad, 0)
    y0 = max(y0 - pad, 0)
    x1 = min(x1 + pad + 1, arr.shape[1])
    y1 = min(y1 + pad + 1, arr.shape[0])
    crop = arr[y0:y1, x0:x1].copy()

    # Make remaining near-white transparent (and watermark on white)
    cr, cg, cb = crop[:, :, 0], crop[:, :, 1], crop[:, :, 2]
    cbright = (cr.astype(np.int16) + cg.astype(np.int16) + cb.astype(np.int16)) / 3.0
    csat = (
        np.maximum(np.maximum(cr, cg), cb).astype(np.int16)
        - np.minimum(np.minimum(cr, cg), cb).astype(np.int16)
    )
    white = (cbright > 242) & (csat < 20)
    crop[white, 3] = 0

    # Soft rounded-rect alpha mask matching app-icon corners
    h, w = crop.shape[:2]
    radius = int(min(h, w) * 0.18)
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=1.2))
    mask_arr = np.array(mask)
    crop[:, :, 3] = (crop[:, :, 3].astype(np.float32) * (mask_arr / 255.0)).astype(np.uint8)

    out = Image.fromarray(crop, "RGBA")
    # Downscale for web use while keeping crispness
    max_side = 512
    if max(out.size) > max_side:
        out.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)
    return out


def main() -> None:
    src_path = find_source()
    src = Image.open(src_path)
    print(f"source: {src_path} size={src.size}")
    out = extract_icon(src)
    print(f"output size={out.size}")
    for path in TARGETS:
        path.parent.mkdir(parents=True, exist_ok=True)
        out.save(path, "PNG", optimize=True)
        print(f"wrote {path} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
