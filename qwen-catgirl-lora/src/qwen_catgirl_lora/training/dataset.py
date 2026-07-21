from __future__ import annotations

from typing import Any

from datasets import load_dataset

from qwen_catgirl_lora.config import resolve_path


def load_train_eval_datasets(cfg: dict[str, Any]):
    data_cfg = cfg["data"]
    data_path = resolve_path(data_cfg["file"])
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {data_path}")

    # 按 9:1 拆分为训练集和验证集（设置随机种子保证可复现）
    dataset = load_dataset("json", data_files=str(data_path))
    split = dataset["train"].train_test_split(
        test_size=data_cfg["test_size"],
        seed=data_cfg["seed"],
    )
    return split["train"], split["test"]


def build_preprocess_fn(tokenizer, cfg: dict[str, Any]):
    data_cfg = cfg["data"]
    max_length = data_cfg["max_length"]
    truncation_side = data_cfg["truncation_side"]
    """将对话或指令格式转化为模型输入"""
    # 数据是 {"instruction": "xxxx", "output": "xxxx"} 格式

    def preprocess_function(examples):
        texts = []
        for inst, out in zip(examples["instruction"], examples["output"]):
            # 构造对话消息列表（无 system 角色）
            messages = [
                {"role": "user", "content": inst},
                {"role": "assistant", "content": out},
            ]
            # 使用 Qwen 的 chat template 生成带特殊 token 的完整文本
            text = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=False,
            )
            texts.append(text)
        
        # 对文本进行分词
        tokenizer.truncation_side = truncation_side
        encodings = tokenizer(
            texts,
            truncation=True,
            padding="max_length",  # 使用padding，配合DataCollator
            max_length=max_length, # 根据你的数据和显存调整[reference:22]
            return_tensors=None,
        )
        # 对于因果语言模型，labels就是input_ids
        encodings["labels"] = encodings["input_ids"].copy()
        return encodings

    return preprocess_function


def tokenize_datasets(train_dataset, eval_dataset, tokenizer, cfg: dict[str, Any]):
    preprocess = build_preprocess_fn(tokenizer, cfg)
    tokenized_train = train_dataset.map(
        preprocess,
        batched=True,
        remove_columns=train_dataset.column_names, # 移除原始 instruction/output 列，节省内存
    )
    tokenized_eval = eval_dataset.map(
        preprocess,
        batched=True,
        remove_columns=eval_dataset.column_names, # 移除原始 instruction/output 列，节省内存
    )
    return tokenized_train, tokenized_eval
