from __future__ import annotations

import json
from pathlib import Path


def json_to_jsonl(json_path: str | Path, jsonl_path: str | Path) -> int:
    """Convert a JSON array dataset file to JSONL format."""
    src = Path(json_path)
    dst = Path(jsonl_path)
    with src.open("r", encoding="utf-8") as f:
        data = json.load(f)

    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    return len(data)
