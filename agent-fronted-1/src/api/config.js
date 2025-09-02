// API配置
const API_CONFIG = {
  development: {
    baseURL: 'http://localhost:8080/api'
  },
  production: {
    baseURL: 'https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api'
  }
}

// 根据当前环境选择配置
const currentEnv = import.meta.env.MODE || 'development'
export const baseURL = API_CONFIG[currentEnv].baseURL

// API端点
export const API_ENDPOINTS = {
  LOVE_APP_CHAT: '/ai/love_app/chat/sse_emitter',
  MANUS_CHAT: '/ai/manus/chat'
}
