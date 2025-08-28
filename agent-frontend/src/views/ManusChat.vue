<template>
  <ChatRoom
    title="AI 超级智能体（Manus）"
    :placeholder="'向 Manus 提问...'"
    :chatId="chatId"
    :initialMessages="messages"
    @messages-change="save"
    @send="handleSend"
    @clear-history="clearHistory"
  />
</template>

<script>
import ChatRoom from '../components/ChatRoom.vue'
import { generateChatId, eventSourceUrl, loadMessages, saveMessagesDebounced, saveMessages, clearMessages } from '../utils/chat'

export default {
  name: 'ManusChat',
  components: { ChatRoom },
  data() {
    return { chatId: generateChatId(), es: null, messages: [] }
  },
  created() {
    this.messages = loadMessages('manus')
  },
  mounted() {
    // 刷新/关闭标签页前强制落盘，避免防抖保存未及时写入
    window.addEventListener('beforeunload', this.flushSave)
  },
  unmounted() {
    window.removeEventListener('beforeunload', this.flushSave)
  },
  methods: {
    save(list) {
      // 同步本地状态，确保 beforeunload/异常保存使用的 this.messages 为最新
      this.messages = Array.isArray(list) ? list : []
      saveMessagesDebounced('manus', this.messages)
    },
    flushSave() {
      try { saveMessages('manus', this.messages) } catch (_) {}
    },
    clearHistory() {
      clearMessages('manus')
      this.messages = []
    },
    handleSend({ text, pushAssistant }) {
      pushAssistant(({ update, done, start }) => {
        start()
        // 后端返回 SseEmitter，GET /ai/manus/chat?message=xxx，按 SSE 协议推送
        const url = eventSourceUrl('/ai/manus/chat', { message: text })
        console.log('Creating SSE connection for Manus chat:', { url, message: text })
        
        const es = new EventSource(url)
        this.es = es
        
        es.onmessage = (e) => {
          const chunk = e.data || ''
          console.log('SSE chunk received for Manus:', chunk)
          console.log('Chunk type:', typeof chunk)
          console.log('Chunk length:', chunk.length)
          
          // 验证chunk数据
          if (chunk && typeof chunk === 'string' && chunk.trim() !== '') {
            update(chunk)
            console.log('Chunk updated successfully for Manus')
          } else {
            console.log('Skipping invalid chunk for Manus:', chunk)
          }
        }
        
        es.onerror = (error) => {
          console.error('SSE Error for Manus:', error)
          es.close()
          done()
          // 结束时强制保存一次，确保落盘
          try { saveMessages('manus', this.messages) } catch (_) {}
        }
        
        es.onopen = () => {
          console.log('SSE connection opened for Manus')
        }
      })
    }
  },
  beforeUnmount() {
    if (this.es) this.es.close()
    try { saveMessages('manus', this.messages) } catch (_) {}
  }
}
</script>

<style scoped>
</style>

 