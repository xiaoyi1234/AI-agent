from pathlib import Path

import yaml

from qwen_catgirl_lora.config import DEFAULT_CONFIG_PATH, PROJECT_ROOT, load_config, resolve_path


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir()
    assert (PROJECT_ROOT / "config" / "default.yaml").exists()


def test_load_default_config():
    cfg = load_config()
    assert "model" in cfg
    assert "training" in cfg
    assert cfg["lora"]["r"] == 16


def test_resolve_relative_path():
    resolved = resolve_path("../NekoQA-10K.jsonl")
    assert resolved.is_absolute()


def test_default_config_file_is_valid_yaml():
    with DEFAULT_CONFIG_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data["data"]["seed"] == 42
