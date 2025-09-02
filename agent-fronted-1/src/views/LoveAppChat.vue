<template>
  <div class="love-app-chat">
    <!-- 页面头部 -->
    <div class="chat-header">
      <div class="header-content">
        <button @click="goBack" class="back-button tech-button">
          <span class="button-icon">←</span>
          返回主页
        </button>
        <div class="title-section">
          <h1>AI PCIE技术应用</h1>
          <p class="subtitle">基于PCIE技术的专业智能对话系统</p>
        </div>
        <div class="chat-info">
          <div class="chat-id-container">
            <span class="chat-id-label">聊天室ID:</span>
            <span class="chat-id">{{ chatId }}</span>
          </div>
          <button @click="clearChat" class="clear-button tech-button">
            <span class="button-icon">🗑️</span>
            清空聊天
          </button>
        </div>
      </div>
    </div>
    
    <!-- 聊天界面 -->
    <ChatInterface 
      :messages="messages" 
      :is-loading="isLoading"
      :ai-type="'pcie'"
      @send-message="handleSendMessage"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chatStore'
import { chatWithLoveApp, generateChatId } from '../api/chatService'
import ChatInterface from '../components/ChatInterface.vue'

const router = useRouter()
const chatStore = useChatStore()

// 响应式数据
const chatId = ref('')
const messages = ref([])
const isLoading = ref(false)
let currentEventSource = null

// 返回主页
const goBack = () => {
  router.push('/')
}

// 清空聊天记录
const clearChat = () => {
  chatStore.clearMessages()
  messages.value = []
  // 生成新的聊天室ID
  chatId.value = generateChatId()
  chatStore.setChatId(chatId.value)
}

// 发送消息
const handleSendMessage = async (message) => {
  if (!message.trim() || isLoading.value) return
  
  // 添加用户消息
  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: message,
    timestamp: new Date().toISOString()
  }
  
  messages.value.push(userMessage)
  chatStore.addMessage(userMessage)
  
  // 设置加载状态
  isLoading.value = true
  chatStore.setLoading(true)
  
  try {
    // 关闭之前的连接
    if (currentEventSource) {
      currentEventSource.close()
    }
    
    // 创建新的SSE连接
    currentEventSource = chatWithLoveApp(
      message,
      chatId.value,
      (data) => {
        // 处理流式响应
        chatStore.addAIStreamMessage(data)
        // 更新本地消息
        const lastMessage = messages.value[messages.value.length - 1]
        if (lastMessage && lastMessage.role === 'assistant') {
          lastMessage.content += data
        } else {
          messages.value.push({
            id: Date.now(),
            role: 'assistant',
            content: data,
            timestamp: new Date().toISOString()
          })
        }
      },
      (error) => {
        console.error('SSE连接错误:', error)
        isLoading.value = false
        chatStore.setLoading(false)
      },
      () => {
        // 连接完成
        isLoading.value = false
        chatStore.setLoading(false)
        currentEventSource = null
      }
    )
  } catch (error) {
    console.error('发送消息失败:', error)
    isLoading.value = false
    chatStore.setLoading(false)
  }
}

// 组件挂载时初始化
onMounted(() => {
  // 生成聊天室ID
  chatId.value = generateChatId()
  chatStore.setChatId(chatId.value)
  
  // 从store恢复消息
  messages.value = [...chatStore.messages]
})

// 组件卸载时清理
onUnmounted(() => {
  if (currentEventSource) {
    currentEventSource.close()
  }
})
</script>

<style scoped>
.love-app-chat {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

.chat-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.chat-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
  pointer-events: none;
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  gap: 20px;
}

.back-button {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 10px 18px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
  font-weight: 500;
  backdrop-filter: blur(10px);
  min-width: 120px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.button-icon {
  margin-right: 6px;
  font-size: 16px;
}

.title-section {
  text-align: center;
  flex: 1;
}

.title-section h1 {
  margin: 0;
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  margin-bottom: 4px;
}

.subtitle {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
  font-weight: 400;
}

.chat-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 12px;
}

.chat-id-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.chat-id-label {
  font-size: 0.8rem;
  opacity: 0.8;
  font-weight: 400;
}

.chat-id {
  font-size: 0.9rem;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.15);
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  font-family: 'Courier New', monospace;
  letter-spacing: 0.5px;
}

.clear-button {
  background: rgba(255, 107, 53, 0.2);
  border: 1px solid rgba(255, 107, 53, 0.4);
  color: white;
  padding: 8px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.8rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
  min-width: 100px;
}

.clear-button:hover {
  background: rgba(255, 107, 53, 0.3);
  border-color: rgba(255, 107, 53, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .chat-header {
    padding: 20px 16px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .title-section {
    order: 1;
  }
  
  .back-button {
    order: 2;
    align-self: flex-start;
  }
  
  .chat-info {
    order: 3;
    align-items: center;
    width: 100%;
  }
  
  .chat-id-container {
    align-items: center;
  }
  
  .back-button,
  .clear-button {
    min-width: auto;
    width: fit-content;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .header-content {
    gap: 16px;
  }
  
  .chat-header {
    padding: 22px;
  }
  
  .title-section h1 {
    font-size: 1.8rem;
  }
}

@media (min-width: 1025px) {
  .header-content {
    max-width: 1200px;
  }
  
  .chat-header {
    padding: 28px;
  }
  
  .title-section h1 {
    font-size: 2.2rem;
  }
}
</style>
