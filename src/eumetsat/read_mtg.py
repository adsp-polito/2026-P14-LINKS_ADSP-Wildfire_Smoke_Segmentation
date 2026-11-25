"""Read, crop, and export Meteosat-12 (MTG-FCI L1c) NetCDF products using Satpy."""

from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np


def extract_product_zip(zip_path: Path, extract_dir: Path | None = None) -> Path:
    """Extract an EUMETSAT .zip product archive and return the extracted folder."""
    target_dir = extract_dir or zip_path.with_suffix("")
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(target_dir)
    return target_dir


def load_fci_scene(product_dir: Path, channels: list[str] | None = None):
    """Load an extracted MTG-FCI L1c folder into a Satpy Scene.

    Common FCI channels for smoke (VIS / NIR / SWIR / TIR):
      - 'vis_04', 'vis_05', 'vis_06', 'vis_08', 'nir_16', 'nir_22', 'ir_38', 'ir_105', 'ir_123'
    """
    try:
        from satpy import Scene
    except ImportError as exc:
        raise ImportError(
            "satpy is required to read MTG-FCI NetCDF files. Install with: pip install satpy netCDF4"
        ) from exc

    nc_files = sorted(str(p) for p in product_dir.rglob("*.nc") if "CHK-TRAIL" not in p.name)
    if not nc_files:
        raise FileNotFoundError(f"No .nc files found in {product_dir}")

    scn = Scene(filenames=nc_files, reader="fci_l1c_nc")
    available = scn.available_dataset_names()
    to_load = channels if channels is not None else [c for c in available if c.startswith(("vis_", "nir_", "ir_"))]
    scn.load(to_load)
    return scn


def crop_and_stack(
    scn,
    channels: list[str],
    lon_bounds: tuple[float, float],
    lat_bounds: tuple[float, float],
    resampler: str = "nearest",
) -> tuple[np.ndarray, dict]:
    """Crop a Satpy Scene to (lon_min, lon_max), (lat_min, lat_max) and stack channels as (C, H, W)."""
    import dask

    cropped = scn.crop(ll_bbox=(lon_bounds[0], lat_bounds[0], lon_bounds[1], lat_bounds[1]))
    # Resample to the coarsest/finest loaded area so all bands share the same (H, W) grid
    resampled = cropped.resample(cropped.finest_area(), resampler=resampler)
    with dask.config.set(scheduler="synchronous"):
        arrays = [np.asarray(resampled[ch].values, dtype=np.float32) for ch in channels]
    stack = np.stack(arrays, axis=0)
    meta = {
        "channels": channels,
        "shape": stack.shape,
        "area": str(resampled.finest_area()),
    }
    return stack, meta
