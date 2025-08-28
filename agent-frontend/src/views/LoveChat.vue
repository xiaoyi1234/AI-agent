<template>
  <ChatRoom
    title="AI PCIE技术顾问应用"
    :placeholder="'向 PCIE 技术顾问提问...'"
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
  name: 'LoveChat',
  components: { ChatRoom },
  data() {
    return { chatId: generateChatId(), es: null, messages: [] }
  },
  created() {
    this.messages = loadMessages('love')
  },
  methods: {
    save(list) {
      this.messages = Array.isArray(list) ? list : []
      saveMessagesDebounced('love', this.messages)
    },
    clearHistory() {
      clearMessages('love')
      this.messages = []
    },
    handleSend({ text, pushAssistant }) {
      pushAssistant(({ update, done, start }) => {
        start()
        const url = eventSourceUrl('/ai/love_app/chat/sse', { message: text, chatId: this.chatId })
        const es = new EventSource(url)
        this.es = es
        es.onmessage = (e) => {
          update(e.data || '')
        }
        es.onerror = () => {
          es.close()
          done()
          // 结束时强制保存一次，确保落盘
          try { saveMessages('love', this.messages) } catch (_) {}
        }
        es.onopen = () => {}
      })
    }
  },
  beforeUnmount() {
    if (this.es) this.es.close()
    try { saveMessages('love', this.messages) } catch (_) {}
  }
}
</script>

<style scoped>
</style>

