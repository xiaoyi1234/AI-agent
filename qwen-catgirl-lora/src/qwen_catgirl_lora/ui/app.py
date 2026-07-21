from __future__ import annotations

from typing import Any

import gradio as gr

from qwen_catgirl_lora.inference.chat import chat
from qwen_catgirl_lora.inference.model import CatgirlChatModel
from qwen_catgirl_lora.ui.css import CUSTOM_CSS


def build_app(model: CatgirlChatModel, cfg: dict[str, Any]) -> gr.Blocks:
    g = cfg["gradio"]

    with gr.Blocks(
        title=g["title"],
        theme=gr.themes.Soft(primary_hue="pink", secondary_hue="rose"),
        css=CUSTOM_CSS,
    ) as demo:
        gr.Markdown(
            """
            # 🐾 喵～ 我是猫娘助手！ 🐾
            ### 基于 QLoRA 微调的 Qwen2.5-7B，已经加载你的专属适配器啦 ✨
            **有什么想和猫娘聊的嘛？(ฅ´ω`ฅ)**
            """
        )
        # 聊天组件（默认 messages 格式）
        chatbot = gr.Chatbot(label="📝 对话记录", height=550, elem_classes="chatbot") # 应用自定义 CSS

        
        with gr.Row():
            msg = gr.Textbox(
                label="✏️ 输入消息",
                placeholder="喵～ 输入你想说的话...",
                scale=4,
            )
            send_btn = gr.Button("🐾 发送", variant="primary", scale=1)

        clear = gr.ClearButton([msg, chatbot], value="🧹 清空对话")

        def respond(message, chat_history):
            new_history, _ = chat(model, message, chat_history)
            return new_history, ""

        msg.submit(respond, [msg, chatbot], [chatbot, msg])
        send_btn.click(respond, [msg, chatbot], [chatbot, msg])

    return demo


def launch_app(model: CatgirlChatModel, cfg: dict[str, Any]) -> None:
    demo = build_app(model, cfg)
    g = cfg["gradio"]
    demo.queue()  # 启用队列处理并发请求
    demo.launch(
        server_name=g["server_name"],
        server_port=g["server_port"],
        share=g["share"],
    )
