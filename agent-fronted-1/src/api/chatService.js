import { baseURL, API_ENDPOINTS } from './config.js'

// 生成唯一的聊天室ID
export const generateChatId = () => {
  return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
}

// 创建SSE连接
export const createSSEConnection = (endpoint, params, onMessage, onError, onComplete) => {
  const url = new URL(baseURL + endpoint)
  
  // 添加查询参数
  Object.keys(params).forEach(key => {
    if (params[key] !== undefined && params[key] !== null) {
      url.searchParams.append(key, params[key])
    }
  })

  const eventSource = new EventSource(url.toString())
  
  eventSource.onmessage = (event) => {
    if (onMessage) {
      onMessage(event.data)
    }
  }
  
  eventSource.onerror = (error) => {
    if (onError) {
      onError(error)
    }
    eventSource.close()
  }
  
  eventSource.addEventListener('complete', () => {
    if (onComplete) {
      onComplete()
    }
    eventSource.close()
  })
  
  return eventSource
}

// LoveApp聊天服务
export const chatWithLoveApp = (message, chatId, onMessage, onError, onComplete) => {
  return createSSEConnection(
    API_ENDPOINTS.LOVE_APP_CHAT,
    { message, chatId },
    onMessage,
    onError,
    onComplete
  )
}

// Manus聊天服务
export const chatWithManus = (message, onMessage, onError, onComplete) => {
  return createSSEConnection(
    API_ENDPOINTS.MANUS_CHAT,
    { message },
    onMessage,
    onError,
    onComplete
  )
}
