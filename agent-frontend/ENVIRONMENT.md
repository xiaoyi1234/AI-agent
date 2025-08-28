# 环境配置说明

## 概述

本项目支持多环境配置，可以根据不同的运行环境自动切换 API 端点。

## 环境配置

### 开发环境 (Development)
- **API 基础 URL**: `http://localhost:8080/api`
- **启动命令**: `npm run dev`
- **说明**: 开发时使用本地后端服务

### 生产环境 (Production)
- **API 基础 URL**: `/api` (相对路径)
- **启动命令**: `npm run build`
- **说明**: 生产环境使用相对路径，适用于前后端部署在同一域名下

## 配置原理

1. **环境变量检测**: 通过 `process.env.NODE_ENV` 检测当前环境
2. **自动切换**: 根据环境自动选择对应的 API 基础 URL
3. **代理配置**: 开发环境通过 Vite 代理将 `/api` 请求转发到本地后端

## 文件结构

```
src/
├── config/
│   └── env.js          # 环境配置文件
└── utils/
    └── chat.js         # API 客户端配置
```

## 使用方法

### 在代码中使用配置

```javascript
import { config } from '../config/env.js'

// 获取 API 基础 URL
console.log(config.api.baseURL)

// 检查当前环境
console.log(config.isProduction)  // true/false
console.log(config.isDevelopment) // true/false
```

### 环境变量设置

- **开发环境**: `NODE_ENV=development` (默认)
- **生产环境**: `NODE_ENV=production`

## 部署说明

### 开发环境
```bash
npm run dev
```

### 生产环境
```bash
npm run build
```

生产环境构建后，需要确保：
1. 前端静态文件部署到 Web 服务器
2. 后端 API 服务运行在 `https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com`
3. 配置反向代理，将 `/api` 路径的请求转发到后端服务

## 注意事项

1. 开发环境使用绝对 URL (`http://localhost:8080/api`)，便于调试
2. 生产环境使用相对 URL (`/api`)，便于部署和域名切换
3. Vite 开发服务器已配置代理，开发时可直接使用 `/api` 路径
