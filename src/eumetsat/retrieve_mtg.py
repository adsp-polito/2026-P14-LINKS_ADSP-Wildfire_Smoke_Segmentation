"""Retrieve Meteosat-12 (MTG-FCI) L1c products from EUMETSAT Data Store via eumdac >= 4.0 (OAuth2 v2).

Required environment variables (EUMETSAT User Portal credentials):
  - EUMDAC_USER
  - EUMDAC_PW
"""

from __future__ import annotations

import os
import shutil
from datetime import datetime
from pathlib import Path

from src.config import load_paths_config, resolve_path

# Default MTG-FCI Level 1c High Spatial Resolution / Full Disc collection ID on EUMETSAT Data Store.
# Verify exact collection ID in eumdac (`datastore.collections`) if your account uses FDHSI vs HRFI.
DEFAULT_MTG_COLLECTION = "EO:EUM:DAT:0662"  # FCI Level 1c Normal Resolution (FDHSI)


def get_eumdac_datastore():
    """Authenticate against EUMETSAT Data Store v2 using EUMDAC_USER and EUMDAC_PW."""
    try:
        from eumdac.datastore import DataStore
        from eumdac.token import Creds, OAuth2Token
    except ImportError as exc:
        raise ImportError(
            "eumdac>=4.0.0 is required for EUMETSAT v2 retrieval. Install it with: pip install 'eumdac>=4.0.0'"
        ) from exc

    user = os.getenv("EUMDAC_USER")
    pw = os.getenv("EUMDAC_PW")
    if not user or not pw:
        raise EnvironmentError(
            "Missing EUMDAC_USER or EUMDAC_PW environment variables."
        )

    token = OAuth2Token().set_credentials(Creds(user=user, pw=pw))
    return DataStore(token)


def list_fci_collections(keyword: str = "FCI") -> list[tuple[str, str]]:
    """List available EUMETSAT collections matching keyword (e.g. 'FCI' or 'MTG')."""
    datastore = get_eumdac_datastore()
    matches: list[tuple[str, str]] = []
    for coll in datastore.collections:
        title = getattr(coll, "title", "") or ""
        if keyword.lower() in str(coll).lower() or keyword.lower() in title.lower():
            matches.append((str(coll), title))
    return matches


def search_mtg_products(
    start: datetime,
    end: datetime,
    collection_id: str = DEFAULT_MTG_COLLECTION,
    bbox: tuple[float, float, float, float] | None = None,
):
    """Search MTG-FCI products in [start, end] optionally filtered by (west, south, east, north)."""
    datastore = get_eumdac_datastore()
    collection = datastore.get_collection(collection_id)
    search_kwargs = {"dtstart": start, "dtend": end}
    if bbox is not None:
        west, south, east, north = bbox
        search_kwargs["geo"] = f"POLYGON(({west} {south},{east} {south},{east} {north},{west} {north},{west} {south}))"
    return list(collection.search(**search_kwargs))


def download_products(products: list, output_dir: Path | None = None, max_items: int | None = None) -> list[Path]:
    """Download selected eumdac products into eumetsat.raw_dir."""
    if output_dir is None:
        cfg = load_paths_config()
        output_dir = resolve_path(cfg["eumetsat"]["raw_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    downloaded: list[Path] = []
    subset = products[:max_items] if max_items is not None else products
    for product in subset:
        target_path = output_dir / f"{product}.zip"
        if target_path.exists():
            downloaded.append(target_path)
            continue
        with product.open() as src, open(target_path, "wb") as dst:
            shutil.copyfileobj(src, dst)
        downloaded.append(target_path)
    return downloaded
