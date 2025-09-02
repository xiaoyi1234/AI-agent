<template>
  <div class="chat-interface">
    <!-- 聊天记录区域 -->
    <div class="chat-messages" ref="messagesContainer">
      <div 
        v-for="message in messages" 
        :key="message.id" 
        :class="['message', message.role === 'user' ? 'user-message' : 'ai-message']"
      >
        <div class="message-content">
          <div class="message-avatar" :class="message.role === 'user' ? 'user-avatar' : 'ai-avatar'">
            <img 
              v-if="message.role === 'assistant'" 
              :src="getAIAvatar()" 
              :alt="getAIAvatarAlt()"
              class="avatar-image"
            />
            <span v-else class="avatar-icon">👤</span>
          </div>
          <div class="message-bubble">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
            <div class="message-time">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
      </div>
      
      <!-- 加载指示器 -->
      <div v-if="isLoading" class="message ai-message">
        <div class="message-content">
          <div class="message-avatar ai-avatar">
            <img :src="getAIAvatar()" :alt="getAIAvatarAlt()" class="avatar-image" />
          </div>
          <div class="message-bubble">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 输入区域 -->
    <div class="chat-input-area">
      <div class="input-container">
        <div class="input-wrapper">
          <textarea
            v-model="inputMessage"
            @keydown.enter.prevent="handleSendMessage"
            placeholder="输入您的消息..."
            class="message-input"
            rows="3"
            :disabled="isLoading"
          ></textarea>
          <div class="input-border"></div>
        </div>
        <button 
          @click="handleSendMessage" 
          class="send-button tech-button"
          :disabled="!inputMessage.trim() || isLoading"
        >
          <span v-if="!isLoading" class="button-text">
            <span class="button-icon">📤</span>
            发送
          </span>
          <span v-else class="button-text">
            <span class="button-icon pulse">⏳</span>
            发送中...
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { useChatStore } from '../stores/chatStore'

const props = defineProps({
  messages: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  aiType: {
    type: String,
    default: 'default' // 'pcie' 或 'manus'
  }
})

const emit = defineEmits(['send-message'])

const chatStore = useChatStore()
const inputMessage = ref('')
const messagesContainer = ref(null)

// 监听消息变化，自动滚动到底部
watch(() => props.messages.length, () => {
  nextTick(() => {
    scrollToBottom()
  })
})

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 发送消息
const handleSendMessage = () => {
  const message = inputMessage.value.trim()
  if (message && !props.isLoading) {
    emit('send-message', message)
    inputMessage.value = ''
  }
}

// 格式化消息内容（支持换行）
const formatMessage = (content) => {
  return content.replace(/\n/g, '<br>')
}

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 获取AI头像
const getAIAvatar = () => {
  if (props.aiType === 'pcie') {
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iMjAiIGZpbGw9InVybCgjZ3JhZGllbnQwX2xpbmVhcl8xXzEpLz4KPHBhdGggZD0iTTIwIDEwQzE0LjQ3NyAxMCAxMCAxNC40NzcgMTAgMjBDMTAgMjUuNTIzIDE0LjQ3NyAzMCAyMCAzMEMyNS41MjMgMzAgMzAgMjUuNTIzIDMwIDIwQzMwIDE0LjQ3NyAyNS41MjMgMTAgMjAgMTBaIiBmaWxsPSJ1cmwoI2dyYWRpZW50MV9saW5lYXJfMV8xKSIvPgo8cGF0aCBkPSJNMTUgMTVDMTUgMTUgMTggMTIgMjAgMTVDMjIgMTIgMjUgMTUgMjUgMTUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xNSAyNUMxNSAyNSAxOCAyMiAyMCAyNUMyMiAyMiAyNSAyNSAyNSAyNSIgc3Ryb2tlPSJ3aGl0ZSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQwX2xpbmVhcl8xXzEiIHgxPSIwIiB5MT0iMCIgeDI9IjQwIiB5Mj0iNDAiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iIzAwZDRmZiIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMwMDk5Y2MiLz4KPC9saW5lYXJHcmFkaWVudD4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDFfbGluZWFyXzFfMSIgeDE9IjAiIHkxPSIwIiB4Mj0iNDAiIHkyPSI0MCIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjZmZmZmZmIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI2YwZjBmMCIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo='
  } else if (props.aiType === 'manus') {
    return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iMjAiIGZpbGw9InVybCgjZ3JhZGllbnQwX2xpbmVhcl8xXzEpLz4KPHBhdGggZD0iTTIwIDEwQzE0LjQ3NyAxMCAxMCAxNC40NzcgMTAgMjBDMTAgMjUuNTIzIDE0LjQ3NyAzMCAyMCAzMEMyNS41MjMgMzAgMzAgMjUuNTIzIDMwIDIwQzMwIDE0LjQ3NyAyNS41MjMgMTAgMjAgMTBaIiBmaWxsPSJ1cmwoI2dyYWRpZW50MV9saW5lYXJfMV8xKSIvPgo8cGF0aCBkPSJNMTUgMTVDMTUgMTUgMTggMTIgMjAgMTVDMjIgMTIgMjUgMTUgMjUgMTUiIHN0cm9rZT0iI2ZmNmIzNSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPHAgZmlsbD0iI2ZmNmIzNSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEwIj5BSSA8L3A+CjxkZWZzPgo8bGluZWFyR3JhZGllbnQgaWQ9ImdyYWRpZW50MF9saW5lYXJfMV8xIiB4MT0iMCIgeTE9IjAiIHgyPSI0MCIgeTI9IjQwIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+CjxzdG9wIHN0b3AtY29sb3I9IiNmZjZiMzUiLz4KPHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIjZWU1YTI0Ii8+CjwvbGluZWFyR3JhZGllbnQ+CjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQxX2xpbmVhcl8xXzEiIHgxPSIwIiB5MT0iMCIgeDI9IjQwIiB5Mj0iNDAiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iI2ZmZmZmZiIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNmMGYwZjAiLz4KPC9saW5lYXJHcmFkaWVudD4KPC9kZWZzPgo8L3N2Zz4K'
  }
  return 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiByeD0iMjAiIGZpbGw9InVybCgjZ3JhZGllbnQwX2xpbmVhcl8xXzEpLz4KPHBhdGggZD0iTTIwIDEwQzE0LjQ3NyAxMCAxMCAxNC40NzcgMTAgMjBDMTAgMjUuNTIzIDE0LjQ3NyAzMCAyMCAzMEMyNS41MjMgMzAgMzAgMjUuNTIzIDMwIDIwQzMwIDE0LjQ3NyAyNS41MjMgMTAgMjAgMTBaIiBmaWxsPSJ1cmwoI2dyYWRpZW50MV9saW5lYXJfMV8xKSIvPgo8cGF0aCBkPSJNMTUgMTVDMTUgMTUgMTggMTIgMjAgMTVDMjIgMTIgMjUgMTUgMjUgMTUiIHN0cm9rZT0iIzAwZDRmZiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPGRlZnM+CjxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZGllbnQwX2xpbmVhcl8xXzEiIHgxPSIwIiB5MT0iMCIgeDI9IjQwIiB5Mj0iNDAiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj4KPHN0b3Agc3RvcC1jb2xvcj0iIzAwZDRmZiIvPgo8c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiMwMDk5Y2MiLz4KPC9saW5lYXJHcmFkaWVudD4KPGxpbmVhckdyYWRpZW50IGlkPSJncmFkaWVudDFfbGluZWFyXzFfMSIgeDE9IjAiIHkxPSIwIiB4Mj0iNDAiIHkyPSI0MCIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPgo8c3RvcCBzdG9wLWNvbG9yPSIjZmZmZmZmIi8+CjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iI2YwZjBmMCIvPgo8L2xpbmVhckdyYWRpZW50Pgo8L2RlZnM+Cjwvc3ZnPgo='
}

// 获取AI头像alt文本
const getAIAvatarAlt = () => {
  if (props.aiType === 'pcie') {
    return 'PCIE AI助手'
  } else if (props.aiType === 'manus') {
    return '超级智能体'
  }
  return 'AI助手'
}
</script>

<style scoped>
.chat-interface {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: var(--bg-primary);
  background-image: 
    radial-gradient(circle at 20% 80%, rgba(0, 212, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 107, 53, 0.05) 0%, transparent 50%);
}

.message {
  margin-bottom: 24px;
  animation: fadeInUp 0.3s ease-out;
}

.message-content {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  max-width: 100%;
}

.user-message .message-content {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.user-avatar {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  box-shadow: var(--glow-primary);
}

.ai-avatar {
  background: linear-gradient(135deg, var(--accent-color), #ff8c42);
  box-shadow: var(--glow-secondary);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-icon {
  font-size: 24px;
  color: white;
}

.message-bubble {
  max-width: 70%;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 16px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  position: relative;
  transition: all 0.3s ease;
}

.user-message .message-bubble {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border-color: var(--primary-color);
  box-shadow: var(--glow-primary);
}

.ai-message .message-bubble {
  background: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--border-color);
}

.message-bubble:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}

.message-text {
  line-height: 1.6;
  word-wrap: break-word;
  font-size: 15px;
}

.ai-message .message-text {
  text-align: left;
}

.user-message .message-text {
  text-align: right;
}

.message-time {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 8px;
  opacity: 0.8;
}

.user-message .message-time {
  color: rgba(255, 255, 255, 0.8);
  text-align: right;
}

.ai-message .message-time {
  color: var(--text-muted);
  text-align: left;
}

.chat-input-area {
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
  padding: 24px;
  position: relative;
}

.chat-input-area::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
}

.input-container {
  display: flex;
  gap: 16px;
  align-items: flex-end;
  max-width: 1200px;
  margin: 0 auto;
}

.input-wrapper {
  flex: 1;
  position: relative;
}

.message-input {
  width: 100%;
  border: none;
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border-radius: 16px;
  padding: 16px 20px;
  font-size: 15px;
  resize: none;
  outline: none;
  transition: all 0.3s ease;
  font-family: inherit;
  line-height: 1.5;
}

.message-input:focus {
  background: var(--bg-secondary);
  box-shadow: 0 0 0 2px var(--primary-color);
}

.message-input:disabled {
  background: var(--bg-tertiary);
  cursor: not-allowed;
  opacity: 0.6;
}

.message-input::placeholder {
  color: var(--text-muted);
}

.input-border {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 1px solid var(--border-color);
  border-radius: 16px;
  pointer-events: none;
  transition: border-color 0.3s ease;
}

.message-input:focus + .input-border {
  border-color: var(--primary-color);
  box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
}

.send-button {
  padding: 16px 28px;
  border-radius: 16px;
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
  white-space: nowrap;
  min-width: 120px;
  height: 56px;
}

.send-button:disabled {
  background: var(--bg-tertiary);
  color: var(--text-muted);
  cursor: not-allowed;
  box-shadow: none;
}

.send-button:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 0 30px rgba(0, 212, 255, 0.5);
}

.button-text {
  display: flex;
  align-items: center;
  gap: 8px;
}

.button-icon {
  font-size: 16px;
}

/* 打字指示器 */
.typing-indicator {
  display: flex;
  gap: 6px;
  align-items: center;
  padding: 8px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--primary-color);
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-messages {
    padding: 15px;
  }
  
  .chat-input-area {
    padding: 20px 15px;
  }
  
  .message-bubble {
    max-width: 85%;
    padding: 14px 18px;
  }
  
  .input-container {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }
  
  .send-button {
    align-self: flex-end;
    width: fit-content;
    min-width: 100px;
    height: 48px;
    padding: 12px 20px;
  }
  
  .message-avatar {
    width: 40px;
    height: 40px;
  }
  
  .avatar-icon {
    font-size: 20px;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .chat-messages {
    padding: 18px;
  }
  
  .chat-input-area {
    padding: 22px;
  }
  
  .message-bubble {
    max-width: 75%;
  }
}

@media (min-width: 1025px) {
  .chat-messages {
    padding: 24px;
  }
  
  .chat-input-area {
    padding: 28px;
  }
  
  .input-container {
    max-width: 1000px;
  }
}
</style>
