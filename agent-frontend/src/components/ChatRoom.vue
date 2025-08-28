<template>
  <div class="chat-wrapper card">
    <div class="chat-header">
      <div class="chat-title">{{ title }}</div>
      <div class="chat-controls">
        <div class="chat-id" title="会话 ID">{{ chatId }}</div>
        <div class="storage-status" :title="storageAvailable ? '会话存储正常' : '会话存储不可用'">
          {{ storageAvailable ? '💾' : '⚠️' }}
        </div>
        <button class="clear-btn" @click="clearHistory" title="清空历史记录">🗑️</button>
      </div>
    </div>

    <div ref="scrollEl" class="chat-messages">
      <div v-for="m in messages" :key="m.id" class="msg" :class="m.role">
        <div class="bubble">
          <template v-if="m.role === 'assistant'">
            <template v-if="isExpanded(m.id)">
              <pre class="text">{{ m.text }}<span v-if="loading && m.id === lastAssistantId" class="cursor">|</span></pre>
              <div class="tools"><button class="toggle" @click="toggleExpand(m.id)">收起</button></div>
            </template>
            <template v-else>
              <pre class="text collapsed">{{ m.text }}<span v-if="loading && m.id === lastAssistantId" class="cursor">|</span></pre>
              <div class="tools"><button class="toggle" @click="toggleExpand(m.id)">展开</button></div>
            </template>
          </template>
          <template v-else>
            <pre class="text">{{ m.text }}</pre>
          </template>
        </div>
      </div>
    </div>

    <form class="chat-input" @submit.prevent="onSend">
      <input
        v-model.trim="input"
        class="input"
        :placeholder="placeholder"
        :disabled="loading"
      />
      <button class="btn" :disabled="loading || !input">发送</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'ChatRoom',
  props: {
    title: { type: String, default: '聊天' },
    placeholder: { type: String, default: '输入消息后回车发送' },
    chatId: { type: String, default: '' },
    initialMessages: { type: Array, default: () => [] }
  },
  emits: ['send', 'messages-change'],
  data() {
    return {
      input: '',
      messages: [],
      loading: false,
      uiExpanded: {},
      storageAvailable: this.checkStorageAvailability()
    }
  },
  mounted() {
    this.$nextTick(this.scrollToBottom)
  },
  watch: {
    initialMessages: {
      handler(val) {
        if (Array.isArray(val)) {
          this.messages = JSON.parse(JSON.stringify(val))
          // 初始加载时默认收起所有助手消息，只显示首行预览
          this.uiExpanded = {}
          for (const m of this.messages) {
            if (m.role === 'assistant') this.uiExpanded[m.id] = false
          }
          this.$nextTick(this.scrollToBottom)
        }
      },
      deep: true,
      immediate: true
    },
    messages: {
      handler(val) {
        this.$emit('messages-change', val)
        this.$nextTick(this.scrollToBottom)
      },
      deep: true
    }
  },
  computed: {
    lastAssistantId() {
      for (let i = this.messages.length - 1; i >= 0; i--) {
        if (this.messages[i].role === 'assistant') return this.messages[i].id
      }
      return null
    }
  },
  methods: {
    checkStorageAvailability() {
      try {
        const test = '__storage_test__'
        sessionStorage.setItem(test, test)
        sessionStorage.removeItem(test)
        return true
      } catch (e) {
        return false
      }
    },
    isExpanded(id) {
      return this.uiExpanded[id] === true
    },
    toggleExpand(id) {
      this.uiExpanded[id] = !this.uiExpanded[id]
    },
    onSend() {
      const text = this.input
      if (!text) return
      this.input = ''
      const userMsg = { id: Date.now() + '_u', role: 'user', text }
      this.messages.push(userMsg)
      this.$emit('send', { text, pushAssistant: this.pushAssistant })
      this.$nextTick(this.scrollToBottom)
    },
    pushAssistant(getter) {
      const id = Date.now() + '_a'
      const msg = { id, role: 'assistant', text: '' }
      this.messages.push(msg)
      this.uiExpanded[id] = false  // 默认收起状态
      
      const update = (chunk) => {
        if (chunk && typeof chunk === 'string') {
          console.log('Updating message with chunk:', chunk)
          msg.text += chunk
          // 强制Vue更新视图
          this.$forceUpdate()
          this.scrollToBottom()
          console.log('Message updated, current text:', msg.text)
        } else {
          console.warn('Invalid chunk received:', chunk)
        }
      }
      
      const done = () => {
        console.log('SSE stream completed')
        this.loading = false
        // 确保最终状态被保存
        this.$forceUpdate()
      }
      
      const start = () => {
        console.log('Starting SSE stream')
        this.loading = true
      }
      
      getter({ update, done, start })
    },
    scrollToBottom() {
      const el = this.$refs.scrollEl
      if (!el) return
      el.scrollTop = el.scrollHeight
    },
    clearHistory() {
      this.$emit('clear-history')
    }
  }
}
</script>

<style scoped>
.chat-wrapper {
  display: grid;
  grid-template-rows: auto 1fr auto;
  height: calc(100vh - 140px);
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.chat-title { font-weight: 600; }
.chat-id { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; opacity: .7; font-size: 12px; }
.chat-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}
.storage-status {
  font-size: 14px;
  opacity: 0.8;
}
.clear-btn {
  background: transparent;
  border: none;
  color: #93c5fd;
  cursor: pointer;
  padding: 0;
  font-size: 16px;
  line-height: 1;
  transition: color 0.2s ease;
}
.clear-btn:hover {
  color: #60a5fa;
}
.chat-messages {
  overflow-y: auto;
  padding: 16px;
}
.msg {
  display: flex;
  margin-bottom: 12px;
}
.msg.user { justify-content: flex-end; }
.msg.assistant { justify-content: flex-start; }
.bubble {
  max-width: 72%;
  padding: 10px 12px;
  border-radius: 12px;
}
.msg.user .bubble { background: #4f46e5; color: white; border-bottom-right-radius: 4px; }
.msg.assistant .bubble { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-bottom-left-radius: 4px; }
.text { 
  margin: 0; 
  font-family: inherit; 
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  word-break: break-word;
  max-width: 100%;
}

.text.collapsed {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chat-input {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 8px;
  padding: 12px;
  border-top: 1px solid rgba(255,255,255,0.06);
}
.tools { margin-top: 6px; display: flex; }
.toggle { background: transparent; border: none; color: #93c5fd; cursor: pointer; padding: 0; font-size: 12px; }
</style>

<style scoped>
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
.cursor { 
  display: inline-block; 
  width: 1ch; 
  animation: blink 1s infinite; 
  color: #93c5fd; 
}
</style>

