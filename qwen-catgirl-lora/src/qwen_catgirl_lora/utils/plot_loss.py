from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


def plot_loss_curve(
    trainer_state_path: str | Path,
    output_image: str | Path | None = None,
    show: bool = True,
) -> dict[str, Any]:
    state_path = Path(trainer_state_path)
    with state_path.open("r", encoding="utf-8") as f:
        state = json.load(f)

    train_steps: list[int] = []
    train_losses: list[float] = []
    eval_steps: list[int] = []
    eval_losses: list[float] = []

    for log in state["log_history"]:
        if "loss" in log and "eval_loss" not in log:
            train_steps.append(log["step"])
            train_losses.append(log["loss"])
        if "eval_loss" in log:
            eval_steps.append(log["step"])
            eval_losses.append(log["eval_loss"])

    plt.figure(figsize=(10, 6))
    plt.plot(
        train_steps,
        train_losses,
        label="Train Loss",
        color="blue",
        alpha=0.6,
        linewidth=1.5,
    )
    plt.plot(
        eval_steps,
        eval_losses,
        label="Eval Loss",
        color="red",
        marker="o",
        linestyle="-",
        linewidth=2,
        markersize=4,
    )
    plt.xlabel("Training Steps", fontsize=12)
    plt.ylabel("Loss", fontsize=12)
    plt.title("QLoRA Fine-tuning Loss Curve (Qwen2.5-7B)", fontsize=14)
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)

    if output_image:
        out = Path(output_image)
        out.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(out, dpi=300, bbox_inches="tight")
        print(f"图片已保存为 {out}")

    if show:
        plt.show()
    else:
        plt.close()

    return {
        "train_points": len(train_losses),
        "eval_points": len(eval_losses),
        "output_image": str(output_image) if output_image else None,
    }
