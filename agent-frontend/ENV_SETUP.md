# 环境变量配置说明

## 问题描述

当前遇到 CORS 错误，因为前端应用尝试直接访问生产环境的后端服务。

## 解决方案

### 方案 1：使用本地后端服务（推荐）

1. **确保本地后端服务运行在 8080 端口**
2. **使用 Vite 代理**（当前配置）
   - 前端请求 `/api/*` 会被代理到 `http://localhost:8080`
   - 避免 CORS 问题

### 方案 2：使用环境变量配置

创建 `.env.development` 文件：

```bash
# 开发环境配置
NODE_ENV=development

# 使用代理（推荐）
VITE_API_BASE_URL=/api

# 或直接指定本地后端
# VITE_API_BASE_URL=http://localhost:8080/api

# 或连接远程后端（需要解决 CORS）
# VITE_API_BASE_URL=https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api
```

### 方案 3：解决远程后端 CORS 问题

如果必须使用远程后端服务，需要：

1. **后端配置 CORS 头**：
   ```
   Access-Control-Allow-Origin: http://localhost:5173
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
   Access-Control-Allow-Headers: Content-Type, Authorization
   ```

2. **或使用浏览器插件**临时禁用 CORS（仅开发时）

## 当前配置状态

- ✅ 环境配置已修正
- ✅ Vite 代理已配置为本地后端
- ✅ 开发环境使用代理避免 CORS 问题
- ✅ 生产环境预览也配置了代理

## 使用步骤

### 开发环境
1. **启动本地后端服务**：
   ```bash
   # 确保后端服务运行在 http://localhost:8080
   ```

2. **启动前端开发服务器**：
   ```bash
   npm run dev
   ```

3. **验证配置**：
   - 前端运行在 `http://localhost:5173`
   - API 请求通过代理转发到 `http://localhost:8080`
   - 避免 CORS 错误

### 生产环境预览
1. **构建生产版本**：
   ```bash
   npm run build
   ```

2. **启动预览服务器**：
   ```bash
   npm run preview
   ```

3. **验证配置**：
   - 前端运行在 `http://localhost:4173`
   - API 请求通过代理转发到 `http://localhost:8080`
   - 避免 CORS 错误
