from __future__ import annotations

from typing import Any

from qwen_catgirl_lora.inference.model import CatgirlChatModel


def normalize_history(history: list) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    for item in history:
        if isinstance(item, dict) and "role" in item and "content" in item:
            content = item["content"]
            if isinstance(content, list):
                content = " ".join(str(part) for part in content if part)
            elif content is None:
                content = ""
            else:
                content = str(content)
            messages.append({"role": item["role"], "content": content})
    return messages


def chat(
    model: CatgirlChatModel,
    message: str,
    history: list | None = None,
) -> tuple[list, str]:
    history = list(history or [])
    messages = normalize_history(history)
    messages.append({"role": "user", "content": str(message)})

    reply = model.generate(messages)

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    return history, ""
