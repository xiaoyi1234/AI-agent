// 环境配置
export const config = {
  // API 基础 URL 配置
  api: {
    // 根据环境变量设置 API 基础 URL
    baseURL: process.env.NODE_ENV === 'production' 
      ? process.env.VITE_PROD_API_URL || '/api' // 生产环境，可通过环境变量配置
      : process.env.VITE_API_BASE_URL || '/api' // 开发环境，优先使用环境变量，否则使用代理
  },
  
  // 环境信息
  env: process.env.NODE_ENV || 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isDevelopment: process.env.NODE_ENV === 'development'
}

// 导出默认配置
export default config
