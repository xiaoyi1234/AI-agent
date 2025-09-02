import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  // 聊天记录
  const messages = ref([])
  
  // 当前聊天室ID
  const currentChatId = ref('')
  
  // 是否正在加载
  const isLoading = ref(false)
  
  // 添加消息
  const addMessage = (message) => {
    messages.value.push(message)
  }
  
  // 添加AI回复（流式）
  const addAIStreamMessage = (content, isComplete = false) => {
    const lastMessage = messages.value[messages.value.length - 1]
    
    if (lastMessage && lastMessage.role === 'assistant' && !isComplete) {
      // 更新现有的AI消息
      lastMessage.content += content
    } else {
      // 创建新的AI消息
      addMessage({
        id: Date.now(),
        role: 'assistant',
        content: content,
        timestamp: new Date().toISOString()
      })
    }
  }
  
  // 清空聊天记录
  const clearMessages = () => {
    messages.value = []
  }
  
  // 设置聊天室ID
  const setChatId = (chatId) => {
    currentChatId.value = chatId
  }
  
  // 设置加载状态
  const setLoading = (loading) => {
    isLoading.value = loading
  }
  
  return {
    messages,
    currentChatId,
    isLoading,
    addMessage,
    addAIStreamMessage,
    clearMessages,
    setChatId,
    setLoading
  }
})
