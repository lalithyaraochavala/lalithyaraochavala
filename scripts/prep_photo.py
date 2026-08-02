"""
prep_photo.py

Prepares a source photo for ASCII conversion:
  1. Removes the background (rembg) so only the subject remains.
  2. Boosts local contrast with CLAHE so a flat, evenly-lit face still
     produces real highlights/shadows once it's downsampled to characters.
  3. Composites onto pure white, so background pixels map to the blank
     end of the ASCII ramp (white -> space character).

Usage:
    python scripts/prep_photo.py path/to/source-photo.jpg

Output:
    scripts/../source-prepped.png  (grayscale, ready for make_ascii_svg.py)
"""
import sys
import os
import io
import numpy as np
import cv2
from PIL import Image

try:
    from rembg import remove
except ImportError:
    remove = None


def prep_photo(input_path: str, output_path: str = "source-prepped.png") -> str:
    with open(input_path, "rb") as f:
        raw = f.read()

    # 1. Background removal
    if remove is not None:
        cutout_bytes = remove(raw)
        cutout = Image.open(io.BytesIO(cutout_bytes)).convert("RGBA")
    else:
        print("WARNING: rembg not installed, skipping background removal.")
        cutout = Image.open(io.BytesIO(raw)).convert("RGBA")

    # 2. Composite onto pure white background
    white_bg = Image.new("RGBA", cutout.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, cutout).convert("L")

    # 3. CLAHE contrast boost (grayscale)
    arr = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    arr_clahe = clahe.apply(arr)

    out_img = Image.fromarray(arr_clahe)
    out_img.save(output_path)
    print(f"Wrote {output_path} ({out_img.size[0]}x{out_img.size[1]})")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py path/to/photo.jpg")
        sys.exit(1)
    prep_photo(sys.argv[1])
