from __future__ import annotations

from typing import Any

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from qwen_catgirl_lora.config import get_model_path, resolve_path

# ================== 4-bit 加载基座模型 ==================
def build_bnb_config(cfg: dict[str, Any]) -> BitsAndBytesConfig:
    q = cfg["quantization"]
    dtype_name = q.get("bnb_4bit_compute_dtype", "bfloat16")
    compute_dtype = getattr(torch, dtype_name)
    return BitsAndBytesConfig(
        load_in_4bit=q["load_in_4bit"],
        bnb_4bit_use_double_quant=q["bnb_4bit_use_double_quant"],
        bnb_4bit_quant_type=q["bnb_4bit_quant_type"],
        bnb_4bit_compute_dtype=compute_dtype,
    )


class CatgirlChatModel:
    """Loads Qwen base model + LoRA adapter for inference."""

    def __init__(self, cfg: dict[str, Any], lora_path: str | Path | None = None):
        self.cfg = cfg
        self.infer_cfg = cfg["inference"]
        base_path = get_model_path(cfg)
        adapter_path = resolve_path(lora_path or self.infer_cfg["lora_path"])
        if not adapter_path.exists():
            raise FileNotFoundError(f"LoRA adapter not found: {adapter_path}")

        self.lora_path = adapter_path
        # ================== 加载分词器 ==================
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_path,
            trust_remote_code=cfg["model"]["trust_remote_code"],
        )
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        base_model = AutoModelForCausalLM.from_pretrained(
            base_path,
            quantization_config=build_bnb_config(cfg),
            device_map="auto",
            trust_remote_code=cfg["model"]["trust_remote_code"],
        )
        # ================== 加载 LoRA 适配器 ==================
        self.model = PeftModel.from_pretrained(base_model, str(adapter_path))
        self.model.eval() # 切换到推理模式

    @property
    def device(self):
        return self.model.device

    # ================== 对话生成函数 ==================
    def generate(
        self,
        messages: list[dict[str, str]],
        max_new_tokens: int | None = None,
        temperature: float | None = None,
    ) -> str:
        """
    messages: list of dict, 格式 [{"role": "user", "content": "你好"}, ...]
        """
        infer = self.infer_cfg
        max_new_tokens = max_new_tokens or infer["max_new_tokens"]
        temperature = temperature if temperature is not None else infer["temperature"]
        # 应用聊天模板
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,   # 在末尾添加 assistant 提示，让模型开始生成
        )
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
        # 生成回复
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=infer["do_sample"],
                top_p=infer["top_p"],
                pad_token_id=self.tokenizer.eos_token_id,
            )
        # 解码时跳过输入部分，只输出新生成的 tokens
        return self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1] :],
            skip_special_tokens=True,
        )
