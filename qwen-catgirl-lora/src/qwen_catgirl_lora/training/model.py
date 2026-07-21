from __future__ import annotations

from typing import Any

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from qwen_catgirl_lora.config import get_model_path

# --- QLoRA 核心: 4-bit 量化配置 ---
def build_bnb_config(cfg: dict[str, Any]) -> BitsAndBytesConfig:
    q = cfg["quantization"]
    dtype_name = q.get("bnb_4bit_compute_dtype", "bfloat16")
    compute_dtype = getattr(torch, dtype_name)
    return BitsAndBytesConfig(
        load_in_4bit=q["load_in_4bit"],                              # 启用4-bit加载[reference:14]
        bnb_4bit_use_double_quant=q["bnb_4bit_use_double_quant"],    # 双重量化，进一步省显存
        bnb_4bit_quant_type=q["bnb_4bit_quant_type"],                # 使用nf4量化类型
        bnb_4bit_compute_dtype=compute_dtype,                        # 计算时使用bfloat16
    )


def load_tokenizer(cfg: dict[str, Any]):
    model_path = get_model_path(cfg)
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=cfg["model"]["trust_remote_code"],
        use_fast=cfg["model"]["use_fast_tokenizer"],
    )

    # 设置pad_token，防止训练时报警告
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def load_base_model(cfg: dict[str, Any]):
    model_path = get_model_path(cfg)
    return AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=build_bnb_config(cfg),              # 应用4-bit量化配置
        device_map="auto",                                      # 自动分配设备
        trust_remote_code=cfg["model"]["trust_remote_code"],
    )


def build_lora_model(cfg: dict[str, Any]):
    model = load_base_model(cfg)
    model = prepare_model_for_kbit_training(model)

    lora = cfg["lora"]
    lora_config = LoraConfig(
        r=lora["r"],                         # 秩(Rank)  对于QLoRA，通常设置为16或32
        lora_alpha=lora["lora_alpha"],       # 缩放因子  一般为r*2
        target_modules=lora["target_modules"], # 目标模块
        lora_dropout=lora["lora_dropout"],    # Dropout率
        bias=lora["bias"],
        task_type=lora["task_type"],
    )
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters() # 输出示例: trainable params: 13,631,488 || all params: 7,628,556,288 || trainable%: 0.1787%
    return model
