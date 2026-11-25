"""Path and configuration utilities for local and Colab environments."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXAMPLE_CONFIG = PROJECT_ROOT / "configs" / "paths.example.yaml"
DEFAULT_LOCAL_CONFIG = PROJECT_ROOT / "configs" / "paths.local.yaml"


def load_paths_config(config_path: Path | None = None) -> dict[str, Any]:
    """Load dataset paths from local YAML config, falling back to example config."""
    target = config_path or (
        DEFAULT_LOCAL_CONFIG if DEFAULT_LOCAL_CONFIG.exists() else DEFAULT_EXAMPLE_CONFIG
    )
    with open(target, "r", encoding="utf-8") as f:
        cfg: dict[str, Any] = yaml.safe_load(f) or {}

    # Allow environment variable overrides (useful in Colab / CI)
    smokeviz = cfg.setdefault("smokeviz", {})
    if env_data := os.getenv("SMOKEVIZ_DATA_DIR"):
        smokeviz["data_dir"] = env_data
    if env_coords := os.getenv("SMOKEVIZ_COORDS_DIR"):
        smokeviz["coords_dir"] = env_coords
    if env_meta := os.getenv("SMOKEVIZ_METADATA_PATH"):
        smokeviz["metadata_path"] = env_meta

    return cfg


def resolve_path(path_str: str | Path) -> Path:
    """Resolve relative paths against PROJECT_ROOT."""
    p = Path(path_str)
    return p if p.is_absolute() else (PROJECT_ROOT / p).resolve()
