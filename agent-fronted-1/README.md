# AI智能体前端应用

这是一个基于Vue3的AI智能体前端应用，提供两个主要的AI聊天功能：AI PCIE技术应用和AI超级智能体应用。

## 功能特性

- 🏠 **主页导航**：美观的应用选择界面
- 🤖 **AI PCIE技术应用**：基于PCIE技术的专业咨询服务
- 🧠 **AI 超级智能体**：多功能智能体系统
- 💬 **实时聊天**：支持SSE流式响应的实时对话
- 📱 **响应式设计**：适配桌面和移动设备
- 🎨 **现代UI**：美观的渐变色彩和动画效果

## 技术栈

- **前端框架**：Vue 3 (Composition API)
- **路由管理**：Vue Router 4
- **状态管理**：Pinia
- **构建工具**：Vite
- **HTTP客户端**：Axios
- **实时通信**：Server-Sent Events (SSE)

## 项目结构

```
src/
├── api/           # API服务和配置
├── components/    # 可复用组件
├── router/        # 路由配置
├── stores/        # 状态管理
├── views/         # 页面组件
├── style.css      # 全局样式
└── main.js        # 应用入口
```

## 安装和运行

### 1. 安装依赖

```bash
npm install
```

### 2. 开发环境运行

```bash
npm run dev
```

应用将在 `http://localhost:3000` 启动

### 3. 生产环境构建

```bash
npm run build
```

### 4. 预览生产构建

```bash
npm run preview
```

## 环境配置

项目支持开发和生产环境配置：

- **开发环境**：`http://localhost:8080/api`
- **生产环境**：`https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api`

环境会根据 `import.meta.env.MODE` 自动切换。

## 使用说明

### 主页
- 访问应用主页，选择要使用的AI应用
- 点击应用卡片进入对应的聊天界面

### AI PCIE技术应用
- 进入后自动生成唯一的聊天室ID
- 支持实时流式对话
- 可清空聊天记录重新开始

### AI 超级智能体
- 同样支持实时流式对话
- 独立的聊天会话管理
- 专业的智能体服务

## API接口

### 1. LoveApp聊天接口
```
GET /ai/love_app/chat/sse_emitter?message={message}&chatId={chatId}
```

### 2. Manus聊天接口
```
GET /ai/manus/chat?message={message}
```

## 开发说明

### 组件设计
- `ChatInterface.vue`：通用的聊天界面组件
- `LoveAppChat.vue`：PCIE技术应用页面
- `ManusChat.vue`：超级智能体页面

### 状态管理
使用Pinia管理聊天状态，包括：
- 聊天记录
- 聊天室ID
- 加载状态

### SSE连接管理
- 自动生成唯一聊天室ID
- 支持连接复用和清理
- 错误处理和重连机制

## 浏览器兼容性

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
