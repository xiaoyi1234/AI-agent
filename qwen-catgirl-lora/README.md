# Qwen Catgirl LoRA

基于 **Qwen2.5-7B-Instruct** 的 QLoRA 微调工程，使用 [NekoQA-10K](https://huggingface.co/datasets) 风格猫娘对话数据，并提供 Gradio 聊天界面。


## 目录结构

```
qwen-catgirl-lora/
├── config/default.yaml      # 统一配置（模型、LoRA、训练、推理、Gradio）
├── src/qwen_catgirl_lora/   # 核心 Python 包
│   ├── training/            # QLoRA 训练
│   ├── inference/           # 模型加载与对话生成
│   ├── ui/                  # Gradio 猫娘界面
│   └── utils/               # 下载、绘图、数据转换、长度统计
├── scripts/                 # 命令行入口脚本
├── tests/                   # 单元测试
├── data/                    # 数据集目录（可选）
└── outputs/                 # 训练输出（gitignore）
```

## 环境准备

# 创建并激活conda环境 (或使用venv)
conda create -n qwen_lora python=3.10 -y
conda activate qwen_lora

# 检测环境支持CUDA 版本( RTX5070ti  CUDA Version: 13.0)
nvidia-smi

```bash
cd qwen-catgirl-lora

# 推荐：可编辑安装
pip install -e .

# 或使用锁定依赖（Windows + CUDA 13.0 环境）
pip install torch==2.13.0+cu130 torchvision==0.28.0+cu130 --index-url https://download.pytorch.org/whl/cu130
pip install -r requirements-lock.txt
```

## 快速开始

### 1. 准备数据

确保 `NekoQA-10K.jsonl` 可用。默认配置指向上级目录：

```yaml
# config/default.yaml
data:
  file: "../NekoQA-10K.jsonl"
```

如需从 JSON 数组转换：

```bash
python -m qwen_catgirl_lora.cli data json-to-jsonl ../NekoQA-10K.json ../NekoQA-10K.jsonl
```

训练前可统计 token 长度，辅助设置 `data.max_length`（见下方「分析 Token 长度」）。

### 2. 下载基座模型（可选）

若本地尚无 `../qwen/Qwen2_5-7B-Instruct`：

```bash
qcl-download
# 或
python scripts/download_model.py
```

### 3. QLoRA 训练

```bash
qcl-train
# 或
python scripts/train.py
```

训练完成后，LoRA 适配器默认保存到 `../my_qlora_adapter`。

### 4. 启动 Gradio 聊天

```bash
qcl-serve
# 或
python scripts/serve.py
# 指定 LoRA 适配器（覆盖 config 中的 inference.lora_path）
python scripts/serve.py --lora-adapter lora-adapter2
qcl-serve --lora-adapter ./outputs/my_qlora_adapter
```

浏览器访问 `http://localhost:7860`。

### 5. 绘制 Loss 曲线

```bash
qcl-plot-loss --no-show
# 或指定 checkpoint
qcl-plot-loss --state ../qwen_qlora_checkpoints/checkpoint-2268/trainer_state.json -o ../loss_curve.png
```

### 6. 分析 Token 长度

按 Qwen 对话格式（`<|im_start|>user` / `<|im_start|>assistant`）统计数据集中每条样本的 token 数，输出最长、平均、90%/95% 分位数，用于确定 `config/default.yaml` 中的 `data.max_length`。

```bash
python scripts/max_length.py --data data/NekoQA-10K.jsonl
# 或使用 CLI
python -m qwen_catgirl_lora.cli max-length --data data/NekoQA-10K.jsonl
# 读取 default.yaml 中的模型与数据路径
python scripts/max_length.py
python -m qwen_catgirl_lora.cli max-length --config config/default.yaml
```

可选参数：

| 参数 | 说明 |
|------|------|
| `--config`, `-c` | YAML 配置路径（默认 `config/default.yaml`） |
| `--data` | JSONL 数据集路径（默认取配置中的 `data.file`） |
| `--model` | 模型名称或本地路径（默认优先使用本地基座模型） |

示例输出（`data/NekoQA-10K.jsonl`）：

```
最长长度: 2247
平均长度: 219.1
90%分位数: 291.0
95%分位数: 343.0
```

实现位于 `src/qwen_catgirl_lora/utils/max_length.py`。

## 配置说明

所有路径与超参数集中在 `config/default.yaml`：

| 区块 | 说明 |
|------|------|
| `model` | 基座模型 ID / 本地路径 |
| `quantization` | 4-bit QLoRA 量化 |
| `lora` | LoRA rank、target_modules 等 |
| `data` | 数据集路径、max_length、划分比例（可用 `max-length` 命令辅助选型） |
| `training` | epoch、batch、学习率、checkpoint |
| `inference` | LoRA 路径、生成参数（LoRA 路径可被 `--lora-adapter` 覆盖） |
| `gradio` | 服务端口与标题 |

使用自定义配置：

```bash
qcl-train --config path/to/my_config.yaml
qcl-serve --config path/to/my_config.yaml
```

## 开发

```bash
pip install -e ".[dev]"
pytest
ruff check src tests
```

## 硬件建议

- **训练**：NVIDIA GPU，建议 ≥ 16GB 显存（4-bit QLoRA + batch_size=8）
- **推理**：4-bit 量化加载，约 6–8GB 显存

## License

MIT
