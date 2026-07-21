CUSTOM_CSS = """
/* 全局背景 - 粉嫩渐变 */
.gradio-container {
    background: linear-gradient(135deg, #ffe6f0 0%, #ffd9e8 100%);
    font-family: 'Comic Sans MS', 'Chalkboard SE', 'Yuanti SC', cursive, sans-serif;
}

h1, h2, h3 {
    color: #d45a8a !important;
    text-shadow: 2px 2px 4px rgba(255, 150, 200, 0.3);
}
h2::before { content: "🐾 "; }
h2::after { content: " 🐾"; }

.chatbot {
    border-radius: 30px !important;
    border: 3px solid #ffb6c1 !important;
    box-shadow: 0 8px 20px rgba(255, 105, 180, 0.2);
    background-color: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(4px);
}

.user-msg {
    background: linear-gradient(135deg, #ffb3c6, #ff8fab) !important;
    color: white !important;
    border-radius: 20px 20px 5px 20px !important;
    padding: 8px 14px !important;
    box-shadow: 0 4px 6px rgba(255, 100, 150, 0.3);
    font-weight: bold;
    margin: 3px 8px !important;
}
.user-msg::before { content: "🐱 "; }

.bot-msg {
    background: linear-gradient(135deg, #e0f0ff, #b8d9ff) !important;
    color: #3d3d5c !important;
    border-radius: 20px 20px 20px 5px !important;
    padding: 4px 10px !important;
    margin: 2px 8px !important;
    max-width: 65% !important;
    word-wrap: break-word !important;
    font-size: 13.5px !important;
    box-shadow: 0 3px 5px rgba(100, 150, 255, 0.15);
}
.bot-msg::before { content: "🌸 "; }

input[type="text"] {
    border-radius: 40px !important;
    border: 2px solid #ff99bb !important;
    padding: 10px 18px !important;
    background: rgba(255, 255, 255, 0.8) !important;
    font-size: 15px !important;
    box-shadow: inset 0 2px 6px rgba(255, 150, 200, 0.15);
}
input[type="text"]:focus {
    border-color: #ff66a3 !important;
    box-shadow: 0 0 0 3px rgba(255, 105, 180, 0.3);
}

button {
    border-radius: 40px !important;
    background: linear-gradient(135deg, #ff99bb, #ff66a3) !important;
    color: white !important;
    border: none !important;
    padding: 8px 20px !important;
    font-weight: bold !important;
    box-shadow: 0 4px 10px rgba(255, 100, 150, 0.4);
    transition: 0.3s;
}
button:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 16px rgba(255, 100, 150, 0.6);
}
button:active { transform: scale(0.96); }

.clear-button { background: #d4a0b0 !important; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #ffe6f0; border-radius: 10px; }
::-webkit-scrollbar-thumb { background: #ff99bb; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #ff66a3; }

.chatbot .message-row { margin: 1px 0 !important; padding: 1px 0 !important; }
.chatbot .message {
    padding: 4px 10px !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
}
.chatbot .message p { margin: 2px 0 !important; }
.chatbot .copy-button,
.chatbot button[data-testid="copy-button"] { display: none !important; }
"""
