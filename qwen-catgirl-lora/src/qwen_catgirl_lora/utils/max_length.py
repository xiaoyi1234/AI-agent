from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from transformers import AutoTokenizer


def build_full_text(instruction: str, output: str) -> str:
    """Build the chat-formatted text fed to the model during training."""
    return (
        f"<|im_start|>user\n{instruction}<|im_end|>\n"
        f"<|im_start|>assistant\n{output}<|im_end|>"
    )


def analyze_max_length(
    data_path: str | Path,
    model_name: str,
    trust_remote_code: bool = True,
    use_fast: bool = False,
) -> dict[str, Any]:
    """Compute token length statistics for instruction/output pairs."""
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=trust_remote_code,
        use_fast=use_fast,
    )

    lengths: list[int] = []
    with Path(data_path).open("r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            full_text = build_full_text(data["instruction"], data["output"])
            lengths.append(len(tokenizer.encode(full_text)))

    stats = {
        "count": len(lengths),
        "max": int(max(lengths)),
        "mean": float(np.mean(lengths)),
        "p90": float(np.percentile(lengths, 90)),
        "p95": float(np.percentile(lengths, 95)),
    }
    return stats


def print_max_length_stats(stats: dict[str, Any]) -> None:
    print(f"最长长度: {stats['max']}")
    print(f"平均长度: {stats['mean']}")
    print(f"90%分位数: {stats['p90']}")
    print(f"95%分位数: {stats['p95']}")
