"""Quick smoke test for EUMETSAT Data Store authentication and MTG-FCI search.

Usage:
  1. Set EUMETSAT_CONSUMER_KEY and EUMETSAT_CONSUMER_SECRET in your environment.
  2. Run: python -m scripts.test_eumetsat_retrieval
"""

from __future__ import annotations

from datetime import datetime, timezone

from src.eumetsat.retrieve_mtg import (
    DEFAULT_MTG_COLLECTION,
    list_fci_collections,
    search_mtg_products,
)


def main() -> None:
    print("1) Checking EUMETSAT Data Store authentication & FCI collections...")
    collections = list_fci_collections("FCI")
    for coll_id, title in collections:
        print(f"   - {coll_id}: {title}")

    print(f"\n2) Searching {DEFAULT_MTG_COLLECTION} for a sample 1-hour window (Mediterranean)...")
    start = datetime(2024, 8, 12, 12, 0, tzinfo=timezone.utc)
    end = datetime(2024, 8, 12, 13, 0, tzinfo=timezone.utc)
    # Example bbox: Greece / Eastern Mediterranean (west, south, east, north)
    products = search_mtg_products(start=start, end=end, bbox=(19.0, 35.0, 29.0, 42.0))
    print(f"   Found {len(products)} products.")
    for p in products[:5]:
        print(f"   - {p}")


if __name__ == "__main__":
    main()
