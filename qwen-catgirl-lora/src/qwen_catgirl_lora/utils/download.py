from __future__ import annotations

from pathlib import Path

from modelscope import snapshot_download


def download_base_model(
    model_id: str = "qwen/Qwen2.5-7B-Instruct",
    cache_dir: str | Path = "./",
) -> str:
    """Download base model from ModelScope."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    model_dir = snapshot_download(model_id, cache_dir=str(cache))
    print(f"Model downloaded to: {model_dir}")
    return model_dir
