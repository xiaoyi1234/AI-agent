from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "default.yaml"


def resolve_path(path: str | Path, base: Path | None = None) -> Path:
    """Resolve a path relative to project root when not absolute."""
    p = Path(path)
    if p.is_absolute():
        return p
    root = base or PROJECT_ROOT
    return (root / p).resolve()


def load_config(config_path: str | Path | None = None) -> dict[str, Any]:
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_model_path(cfg: dict[str, Any]) -> str:
    """Prefer local base model path when it exists, otherwise use remote name."""
    local_path = resolve_path(cfg["model"]["local_path"])
    if local_path.exists():
        return str(local_path)
    return cfg["model"]["name"]
