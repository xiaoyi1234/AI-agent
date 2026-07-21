from __future__ import annotations

from typing import Any
import numpy as np
from transformers import TrainingArguments
from transformers.trainer import Trainer

from qwen_catgirl_lora.config import resolve_path
from qwen_catgirl_lora.training.dataset import load_train_eval_datasets, tokenize_datasets
from qwen_catgirl_lora.training.model import build_lora_model, load_tokenizer
from sklearn.metrics import accuracy_score

# ==================== 4. 配置训练参数并开始训练 ====================
def build_training_args(cfg: dict[str, Any]) -> TrainingArguments:
    t = cfg["training"]
    return TrainingArguments(
        output_dir=str(resolve_path(t["output_dir"])),         
        num_train_epochs=t["num_train_epochs"],                        # 训练轮数
        per_device_train_batch_size=t["per_device_train_batch_size"],  # 根据显存调整，建议从2或4开始
        gradient_accumulation_steps=t["gradient_accumulation_steps"],  # 梯度累积，等效batch size=16
        learning_rate=t["learning_rate"],                              # LoRA/QLoRA推荐学习率
        fp16=t["fp16"],
        gradient_checkpointing=t["gradient_checkpointing"],            # 启用混合精度训练以节省显存
        logging_steps=t["logging_steps"],
        report_to=t["report_to"],                                      # 禁用wandb等日志上报
        eval_strategy=t["eval_strategy"],                              # 按步数评估（也可设为 "epoch"）
        eval_steps=t["eval_steps"],                                    # 每 50 步在验证集上计算一次 loss
        save_strategy=t["save_strategy"],                              # 保存策略必须与 eval_strategy 对齐
        save_steps=t["save_steps"],                                    # 每 50 步保存一次检查点
        save_total_limit=t["save_total_limit"],
        load_best_model_at_end=t["load_best_model_at_end"],            # 训练结束后，自动加载验证集 loss 最低的模型
        metric_for_best_model=t["metric_for_best_model"],              # 以验证集损失为评判标准
        greater_is_better=t["greater_is_better"],                      # loss 越小越好
    )

# 定义准确率指标计算函数
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    # 注意：需要过滤掉 -100 的标签（即padding部分）
    mask = labels != -100
    return {"accuracy": accuracy_score(labels[mask], predictions[mask])}


def run_training(cfg: dict[str, Any]) -> None:
    tokenizer = load_tokenizer(cfg)
    model = build_lora_model(cfg)

    train_dataset, eval_dataset = load_train_eval_datasets(cfg)
    print(f"训练集大小: {len(train_dataset)}")
    print(f"验证集大小: {len(eval_dataset)}")

    tokenized_train, tokenized_eval = tokenize_datasets(
        train_dataset, eval_dataset, tokenizer, cfg
    )

    trainer = Trainer(
        model=model,
        args=build_training_args(cfg),
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        processing_class=tokenizer,
        data_collator=None,                      # 使用默认的DataCollator
        #compute_metrics=compute_metrics,        # 添加准确率指标
    )
    # 开始训练
    trainer.train()

    # ==================== 5. 保存模型 ====================
    adapter_dir = resolve_path(cfg["training"]["adapter_output_dir"])
    adapter_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(str(adapter_dir))
    tokenizer.save_pretrained(str(adapter_dir))
    print(f"LoRA adapter saved to: {adapter_dir}")
