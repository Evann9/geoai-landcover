"""
GeoAI mini project - Week 1: LandCover.ai v1 data exploration

What this script does
  1. Prints metadata (CRS, resolution, size) for every image/mask pair
  2. Counts pixels per class across all masks -> shows class imbalance
  3. Saves a side-by-side preview (image | mask) of one tile
  4. Writes the metadata table to week1_metadata.csv

Usage
  pip install rasterio numpy matplotlib pandas
  python week1_explore.py --root ./landcover.ai.v1

Expected folder layout after unzipping landcover.ai.v1.zip
  landcover.ai.v1/
    images/*.tif   (3-band RGB GeoTIFF, EPSG:2180)
    masks/*.tif    (1-band GeoTIFF, same file names)
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from matplotlib.colors import ListedColormap
from rasterio.enums import Resampling

CLASSES = {0: "background", 1: "building", 2: "woodland", 3: "water", 4: "road"}
COLORS = ["#000000", "#614a4a", "#267300", "#00c5ff", "#cfcfcf"]


def describe_pairs(root: Path) -> pd.DataFrame:
    rows = []
    for img_path in sorted((root / "images").glob("*.tif")):
        mask_path = root / "masks" / img_path.name
        with rasterio.open(img_path) as src:
            row = {
                "file": img_path.name,
                "crs": str(src.crs),
                "width": src.width,
                "height": src.height,
                "bands": src.count,
                "pixel_size_m": round(abs(src.transform.a), 3),
                "area_km2": round(src.width * src.height * abs(src.transform.a * src.transform.e) / 1e6, 3),
                "has_mask": mask_path.exists(),
            }
        rows.append(row)
    return pd.DataFrame(rows)


def count_classes(root: Path) -> pd.Series:
    totals = np.zeros(len(CLASSES), dtype=np.int64)
    for mask_path in sorted((root / "masks").glob("*.tif")):
        with rasterio.open(mask_path) as src:
            mask = src.read(1)
        totals += np.bincount(mask.ravel(), minlength=len(CLASSES))[: len(CLASSES)]
    return pd.Series(totals, index=[CLASSES[i] for i in range(len(CLASSES))])


def save_preview(root: Path, file_name: str, out_path: Path, max_side: int = 1500) -> None:
    img_path = root / "images" / file_name
    mask_path = root / "masks" / file_name

    with rasterio.open(img_path) as src:
        scale = max(src.width, src.height) / max_side
        out_shape = (int(src.height / scale), int(src.width / scale))
        img = src.read(out_shape=(src.count, *out_shape), resampling=Resampling.bilinear)
    with rasterio.open(mask_path) as src:
        mask = src.read(1, out_shape=out_shape, resampling=Resampling.nearest)

    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    axes[0].imshow(np.moveaxis(img[:3], 0, -1))
    axes[0].set_title(f"Image: {file_name}")
    axes[1].imshow(mask, cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="none")
    axes[1].set_title("Mask (0 bg, 1 building, 2 woodland, 3 water, 4 road)")
    for ax in axes:
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("./landcover.ai.v1"))
    args = parser.parse_args()

    meta = describe_pairs(args.root)
    if meta.empty:
        raise SystemExit(f"No .tif files found in {args.root / 'images'}. Check --root.")

    print("=== Metadata ===")
    print(meta.to_string(index=False))
    print(f"\nImages: {len(meta)} | CRS values: {meta['crs'].unique().tolist()}")
    print(f"Pixel sizes (m): {sorted(meta['pixel_size_m'].unique().tolist())}")
    print(f"Total area: {meta['area_km2'].sum():.2f} km2")
    meta.to_csv("week1_metadata.csv", index=False)

    print("\n=== Class pixel ratio (all masks) ===")
    counts = count_classes(args.root)
    ratio = (counts / counts.sum() * 100).round(2)
    print(pd.DataFrame({"pixels": counts, "percent": ratio}).to_string())

    save_preview(args.root, meta.iloc[0]["file"], Path("week1_preview.png"))
    print("\nSaved: week1_metadata.csv, week1_preview.png")


if __name__ == "__main__":
    main()
