<template>
  <div class="typewriter-chat">
    <div class="chat-header">
      <h2>AI应用（打字机效应版）</h2>
      <div class="chat-info">
        <span class="chat-id">会话ID: {{ chatId }}</span>
        <button class="clear-btn" @click="clearHistory">🗑️</button>
      </div>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div v-for="message in messages" :key="message.id" class="message" :class="message.role">
        <div class="message-content">
          <div class="message-text">
            {{ message.text }}
            <span v-if="isTyping && message.role === 'assistant' && message.id === currentTypingMessageId" class="cursor">|</span>
          </div>
          <div class="message-time">{{ formatTime(message.timestamp) }}</div>
        </div>
      </div>
    </div>

    <div class="chat-input-container">
      <form @submit.prevent="sendMessage" class="chat-input-form">
        <input
          v-model="inputMessage"
          type="text"
          placeholder="输入消息..."
          :disabled="isTyping"
          class="chat-input"
          ref="inputField"
        />
        <button type="submit" :disabled="isTyping || !inputMessage.trim()" class="send-btn">
          发送
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { generateChatId, eventSourceUrl, loadMessages, saveMessagesDebounced, clearMessages } from '../utils/chat'

export default {
  name: 'TypewriterChat',
  data() {
    return {
      chatId: generateChatId(),
      messages: [],
      inputMessage: '',
      isTyping: false,
      eventSource: null,
      typewriterSpeed: 50,
      currentTypingMessageId: null,
      pendingBuffer: '',
      typewriterTimer: null,
      sseActive: false
    }
  },
  created() {
    this.messages = loadMessages('typewriter')
  },
  mounted() {
    this.focusInput()
    this.scrollToBottom()
  },
  methods: {
    formatTime(timestamp) {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      })
    },
    focusInput() {
      this.$nextTick(() => {
        if (this.$refs.inputField) {
          this.$refs.inputField.focus()
        }
      })
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messagesContainer
        if (container) {
          container.scrollTop = container.scrollHeight
        }
      })
    },
    addMessage(role, text, timestamp = Date.now()) {
      const message = {
        id: Date.now() + '_' + role,
        role,
        text,
        timestamp
      }
      this.messages.push(message)
      this.saveMessages()
      this.scrollToBottom()
      return message
    },
    beginTypingSession() {
      const assistantMessage = this.addMessage('assistant', '', Date.now())
      this.currentTypingMessageId = assistantMessage.id
      this.isTyping = true
      if (this.typewriterTimer) clearInterval(this.typewriterTimer)
      this.typewriterTimer = setInterval(() => {
        if (this.pendingBuffer && this.pendingBuffer.length > 0) {
          const nextChar = this.pendingBuffer[0]
          this.pendingBuffer = this.pendingBuffer.slice(1)
          const currentMessage = this.messages.find(m => m.id === this.currentTypingMessageId)
          if (currentMessage) {
            currentMessage.text += nextChar
            this.scrollToBottom()
            this.saveMessages()
          }
        } else if (!this.sseActive) {
          this.stopTypingSession()
        }
      }, this.typewriterSpeed)
    },
    stopTypingSession() {
      if (this.typewriterTimer) {
        clearInterval(this.typewriterTimer)
        this.typewriterTimer = null
      }
      this.isTyping = false
      this.currentTypingMessageId = null
      this.pendingBuffer = ''
      this.saveMessages()
    },
    async sendMessage() {
      const message = this.inputMessage.trim()
      if (!message || this.isTyping) return

      this.addMessage('user', message)
      this.inputMessage = ''
      this.focusInput()
      this.startSSEConnection(message)
    },
    startSSEConnection(message) {
      const url = eventSourceUrl('/ai/love_app/chat/sse_emitter', { 
        message: message, 
        chatId: this.chatId 
      })
      
      this.eventSource = new EventSource(url)
      this.sseActive = true

      this.eventSource.onmessage = (event) => {
        const chunk = event.data
        if (!this.isTyping) this.beginTypingSession()
        this.pendingBuffer += chunk
      }

      this.eventSource.onerror = (error) => {
        console.error('SSE Error:', error)
        this.sseActive = false
        if (!this.isTyping) this.saveMessages()
        if (this.eventSource) {
          this.eventSource.close()
          this.eventSource = null
        }
        // 让打字机在缓冲区清空后自行停止
      }
      this.eventSource.onopen = () => { this.sseActive = true }
    },
    saveMessages() {
      saveMessagesDebounced('typewriter', this.messages)
    },
    clearHistory() {
      clearMessages('typewriter')
      this.messages = []
      this.isTyping = false
      this.currentTypingMessageId = null
      if (this.eventSource) {
        this.eventSource.close()
        this.eventSource = null
      }
    }
  },
  beforeUnmount() {
    if (this.eventSource) {
      this.eventSource.close()
    }
  }
}
</script>

<style scoped>
.typewriter-chat {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 140px);
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 12px;
  overflow: hidden;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  background: rgba(255,255,255,0.02);
}

.chat-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.chat-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.chat-id {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  font-size: 12px;
  opacity: 0.7;
}

.clear-btn {
  background: transparent;
  border: none;
  color: #93c5fd;
  cursor: pointer;
  padding: 4px;
  font-size: 16px;
  line-height: 1;
  transition: color 0.2s ease;
  border-radius: 4px;
}

.clear-btn:hover {
  color: #60a5fa;
  background: rgba(255,255,255,0.05);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
  justify-content: flex-end;
}

.message.assistant {
  align-self: flex-start;
  justify-content: flex-start;
}

.message-content {
  padding: 12px 16px;
  border-radius: 18px;
  position: relative;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message.user .message-content {
  background: #4f46e5;
  color: white;
  border-bottom-right-radius: 6px;
}

.message.assistant .message-content {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-bottom-left-radius: 6px;
}

.message-text {
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 4px;
}

.message-time {
  font-size: 11px;
  opacity: 0.6;
  text-align: right;
}

.message.user .message-time {
  text-align: right;
}

.message.assistant .message-time {
  text-align: left;
}

.cursor {
  animation: blink 1s infinite;
  color: #4f46e5;
  font-weight: bold;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.chat-input-container {
  padding: 16px 20px;
  border-top: 1px solid rgba(255,255,255,0.06);
  background: rgba(255,255,255,0.02);
}

.chat-input-form {
  display: flex;
  gap: 12px;
}

.chat-input {
  flex: 1;
  padding: 12px 16px;
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 24px;
  background: rgba(255,255,255,0.04);
  color: #e2e8f0;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s ease;
}

.chat-input:focus {
  border-color: #4f46e5;
}

.chat-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-btn {
  padding: 12px 20px;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 24px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease;
  min-width: 80px;
}

.send-btn:hover:not(:disabled) {
  background: #4338ca;
}

.send-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: rgba(255,255,255,0.02);
}

.chat-messages::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: rgba(255,255,255,0.2);
}
</style>
