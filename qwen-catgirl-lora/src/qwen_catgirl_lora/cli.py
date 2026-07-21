from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from qwen_catgirl_lora.config import get_model_path, load_config, resolve_path

app = typer.Typer(help="Qwen Catgirl LoRA CLI")
train_app = typer.Typer(help="Train QLoRA adapter")
serve_app = typer.Typer(help="Launch Gradio chat UI")
plot_loss_app = typer.Typer(help="Plot training loss curve")
max_length_app = typer.Typer(help="Analyze dataset token lengths")
download_app = typer.Typer(help="Download base model from ModelScope")
data_app = typer.Typer(help="Dataset utilities")


def _load_cfg(config: Optional[Path]) -> dict:
    return load_config(config)


@train_app.callback(invoke_without_command=True)
def train_cmd(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to YAML config"),
) -> None:
    """Run QLoRA fine-tuning."""
    from qwen_catgirl_lora.training.train import run_training

    run_training(_load_cfg(config))


@serve_app.callback(invoke_without_command=True)
def serve_cmd(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to YAML config"),
    lora_adapter: Optional[Path] = typer.Option(
        None,
        "--lora-adapter",
        help="LoRA adapter path (overrides inference.lora_path in config)",
    ),
) -> None:
    """Launch Gradio inference UI."""
    from qwen_catgirl_lora.inference.model import CatgirlChatModel
    from qwen_catgirl_lora.ui.app import launch_app

    cfg = _load_cfg(config)
    model = CatgirlChatModel(cfg, lora_path=lora_adapter)
    print(f"Loaded LoRA adapter: {model.lora_path}")
    launch_app(model, cfg)


@plot_loss_app.callback(invoke_without_command=True)
def plot_loss_cmd(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to YAML config"),
    state: Optional[Path] = typer.Option(None, "--state", help="Path to trainer_state.json"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output PNG path"),
    no_show: bool = typer.Option(False, "--no-show", help="Do not open matplotlib window"),
) -> None:
    """Plot train/eval loss from trainer_state.json."""
    from qwen_catgirl_lora.utils.plot_loss import plot_loss_curve

    cfg = _load_cfg(config)
    plot_cfg = cfg["plot"]
    state_path = state or resolve_path(plot_cfg["trainer_state"])
    output_path = output or resolve_path(plot_cfg["output_image"])
    result = plot_loss_curve(state_path, output_path, show=not no_show)
    print(f"训练 Loss 点数: {result['train_points']}")
    print(f"验证 Loss 点数: {result['eval_points']}")


@max_length_app.callback(invoke_without_command=True)
def max_length_cmd(
    config: Optional[Path] = typer.Option(None, "--config", "-c", help="Path to YAML config"),
    data: Optional[Path] = typer.Option(None, "--data", help="Path to JSONL dataset"),
    model: Optional[str] = typer.Option(None, "--model", help="Model name or local path"),
) -> None:
    """Print token length statistics for the training dataset."""
    from qwen_catgirl_lora.utils.max_length import analyze_max_length, print_max_length_stats

    cfg = _load_cfg(config)
    model_cfg = cfg["model"]
    data_path = data or resolve_path(cfg["data"]["file"])
    model_name = model or get_model_path(cfg)
    stats = analyze_max_length(
        data_path=data_path,
        model_name=model_name,
        trust_remote_code=model_cfg["trust_remote_code"],
        use_fast=model_cfg["use_fast_tokenizer"],
    )
    print_max_length_stats(stats)


@download_app.callback(invoke_without_command=True)
def download_cmd(
    model_id: str = typer.Option("qwen/Qwen2.5-7B-Instruct", "--model-id"),
    cache_dir: Path = typer.Option(Path("./"), "--cache-dir"),
) -> None:
    """Download Qwen base model via ModelScope."""
    from qwen_catgirl_lora.utils.download import download_base_model

    download_base_model(model_id=model_id, cache_dir=cache_dir)


@data_app.command("json-to-jsonl")
def json_to_jsonl_cmd(
    input_path: Path = typer.Argument(..., help="Input JSON file"),
    output_path: Path = typer.Argument(..., help="Output JSONL file"),
) -> None:
    """Convert NekoQA JSON array to JSONL."""
    from qwen_catgirl_lora.utils.data_convert import json_to_jsonl

    count = json_to_jsonl(input_path, output_path)
    print(f"Converted {count} records -> {output_path}")


app.add_typer(train_app, name="train")
app.add_typer(serve_app, name="serve")
app.add_typer(plot_loss_app, name="plot-loss")
app.add_typer(max_length_app, name="max-length")
app.add_typer(download_app, name="download")
app.add_typer(data_app, name="data")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
