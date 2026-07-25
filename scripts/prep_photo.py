"""
prep_photo.py
Turns a source photo into a clean, high-contrast grayscale image ready
for ASCII conversion. Run locally, once, whenever you change your photo.

Usage:
    python scripts/prep_photo.py source-photo.jpg
"""
import sys
import cv2
import numpy as np
from PIL import Image


def prep(src_path: str, out_path: str = "data/prepped.png", size: int = 640):
    img = cv2.imread(src_path)
    if img is None:
        raise SystemExit(f"Could not read {src_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # square crop around the center, then resize
    h, w = gray.shape
    side = min(h, w)
    y0, x0 = (h - side) // 2, (w - side) // 2
    gray = gray[y0:y0 + side, x0:x0 + side]
    gray = cv2.resize(gray, (size, size), interpolation=cv2.INTER_AREA)

    # CLAHE: local contrast so a flatly-lit face gets real highlights/shadows
    clahe = cv2.createCLAHE(clipLimit=2.6, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # gentle denoise so the ASCII ramp doesn't pick up sensor noise
    gray = cv2.bilateralFilter(gray, d=7, sigmaColor=50, sigmaSpace=50)

    Image.fromarray(gray).save(out_path)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: prep_photo.py <source-photo>")
    prep(sys.argv[1])
