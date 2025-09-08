# Test1 - AI Agent 项目

## 项目简介

Test1 是一个基于 Spring Boot 的 AI Agent 项目，集成了多种 AI 模型调用方式、RAG（检索增强生成）功能、聊天记忆管理以及各种实用工具。

## 项目结构

```
src/
├── main/
│   ├── java/
│   │   └── com/xiaoyi/test1/
│   │       ├── Adviser/                    # 切面编程相关
│   │       │   ├── MylogAdvisor.java      # 日志切面
│   │       │   └── ReReadingAdvisor.java  # 重读切面
│   │       ├── agent/                      # AI Agent 核心模块
│   │       │   ├── BaseAgent.java         # 基础 Agent 类
│   │       │   ├── model/
│   │       │   │   └── AgentState.java    # Agent 状态模型
│   │       │   ├── ReActAgent.java        # ReAct 模式 Agent
│   │       │   ├── ToolCallAgent.java     # 工具调用 Agent
│   │       │   └── XiaoyiMaus.java        # 主要 Agent 实现
│   │       ├── App/                        # 应用模块
│   │       │   └── LoveApp.java           # 主要应用类
│   │       ├── Chatmemory/                 # 聊天记忆管理
│   │       │   └── FileBasedChatMemory.java # 基于文件的聊天记忆
│   │       ├── config/                     # 配置类
│   │       │   └── CorsConfig.java        # CORS 跨域配置
│   │       ├── constant/                   # 常量定义
│   │       │   └── FileConstant.java      # 文件相关常量
│   │       ├── controller/                 # 控制器层
│   │       │   ├── AiController.java      # AI 相关接口控制器
│   │       │   └── HealthController.java  # 健康检查控制器
│   │       ├── demo/                       # 演示和测试模块
│   │       │   └── invoke/                # AI 模型调用示例
│   │       │       ├── DashScopeClient.java    # 阿里云 DashScope 客户端
│   │       │       ├── HttpInvoke.java         # HTTP 调用示例
│   │       │       ├── OllamaAiInvoke.java     # Ollama 本地模型调用
│   │       │       ├── SDKInvoke.java          # SDK 调用示例
│   │       │       ├── SpringAiAiInvoke.java   # Spring AI 调用
│   │       │       └── TestApikey.java         # API Key 测试
│   │       ├── rag/                        # RAG 检索增强生成模块
│   │       │   ├── LoveAppContextualQueryAugmenterFactory.java # 上下文查询增强器工厂
│   │       │   ├── LoveAppDocumentLoader.java                 # 文档加载器
│   │       │   ├── LoveAppRagCloudAdvisorConfig.java          # RAG 云配置
│   │       │   ├── LoveAppRagCustomAdvisorFactory.java        # 自定义 RAG 顾问工厂
│   │       │   ├── LoveAppVectorStoreConfig.java              # 向量存储配置
│   │       │   ├── MyKeywordEnricher.java                     # 关键词增强器
│   │       │   ├── MyTokenTextSplitter.java                   # 文本分割器
│   │       │   ├── PgVectorVectorStoreConfig.java             # PostgreSQL 向量存储配置
│   │       │   └── QueryRewriter.java                         # 查询重写器
│   │       ├── tools/                      # 工具模块
│   │       │   ├── FileOperationTool.java     # 文件操作工具
│   │       │   ├── PDFGenerationTool.java     # PDF 生成工具
│   │       │   ├── ResourceDownloadTool.java  # 资源下载工具
│   │       │   ├── TerminalOperationTool.java # 终端操作工具
│   │       │   ├── TerminateTool.java         # 终止工具
│   │       │   ├── ToolRegistration.java      # 工具注册
│   │       │   ├── WebScrapingTool.java       # 网页抓取工具
│   │       │   └── WebSearchTool.java         # 网页搜索工具
│   │       └── Test1Application.java       # 主启动类
│   └── resources/
│       ├── application.yml                 # 主配置文件
│       ├── application-local.yml           # 本地环境配置
│       ├── mcp-servers.json               # MCP 服务器配置
│       ├── document/                       # 文档资源
│       │   ├── pcie-gen4.md               # PCIe Gen4 文档
│       │   ├── pcie-gen5.md               # PCIe Gen5 文档
│       │   └── pcie-gen6.md               # PCIe Gen6 文档
│       ├── static/                         # 静态资源
│       └── templates/                      # 模板文件
└── test/                                   # 测试代码
    └── java/
        └── com/xiaoyi/test1/
            ├── agent/
            │   └── XiaoyiMausTest.java     # Agent 测试
            ├── app/
            │   └── LoveAppTest.java        # 应用测试
            ├── rag/
            │   ├── LoveAppDocumentLoaderTest.java    # 文档加载器测试
            │   └── PgVectorVectorStoreConfigTest.java # 向量存储测试
            └── tools/                      # 工具测试
                ├── FileOperationToolTest.java
                ├── PDFGenerationToolTest.java
                ├── ResourceDownloadToolTest.java
                ├── TerminalOperationToolTest.java
                ├── WebScrapingToolTest.java
                └── WebSearchToolTest.java
```

## 主要功能特性

### 🤖 AI Agent 系统
- **多种 Agent 模式**: 支持 ReAct、工具调用等多种 Agent 模式
- **状态管理**: 完整的 Agent 状态管理机制
- **工具集成**: 丰富的工具集支持

### 🔍 RAG 检索增强生成
- **文档处理**: 支持多种文档格式的加载和处理
- **向量存储**: 集成 PostgreSQL 向量存储
- **查询增强**: 智能查询重写和关键词增强

### 🛠️ 工具生态
- **文件操作**: 文件读写、PDF 生成等
- **网络工具**: 网页抓取、搜索、资源下载
- **系统工具**: 终端操作、进程管理

### 🌐 AI 模型集成
- **多模型支持**: 支持 DashScope、Ollama、Spring AI 等
- **灵活调用**: HTTP、SDK 等多种调用方式
- **本地部署**: 支持 Ollama 等本地模型

### 💬 聊天记忆
- **持久化存储**: 基于文件的聊天历史记录
- **上下文管理**: 智能上下文维护

## 技术栈

- **后端框架**: Spring Boot
- **AI 集成**: Spring AI、DashScope、Ollama
- **向量数据库**: PostgreSQL + pgvector
- **构建工具**: Maven
- **Java 版本**: 8+

## 快速开始

### 环境要求
- Java 8+
- Maven 3.6+
- PostgreSQL 12+ (用于向量存储)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone [项目地址]
   cd Test1
   ```

2. **配置数据库**
   - 安装 PostgreSQL
   - 安装 pgvector 扩展
   - 创建数据库并配置连接信息

3. **配置环境**
   - 复制 `application-local.yml` 并修改配置
   - 配置 AI 模型的 API Key

4. **启动应用**
   ```bash
   mvn spring-boot:run
   ```

### 配置说明

主要配置文件位于 `src/main/resources/` 目录：
- `application.yml`: 主配置文件
- `application-local.yml`: 本地开发配置
- `mcp-servers.json`: MCP 服务器配置

## API 接口

### AI 相关接口
- `POST /ai/chat`: AI 聊天接口
- `POST /ai/rag`: RAG 检索增强接口

### 健康检查
- `GET /health`: 应用健康状态

## 开发指南

### 添加新工具
1. 在 `tools/` 包下创建新的工具类
2. 实现必要的接口方法
3. 在 `ToolRegistration.java` 中注册工具
4. 编写相应的测试用例

### 扩展 Agent 功能
1. 继承 `BaseAgent` 类
2. 实现特定的 Agent 逻辑
3. 在 `XiaoyiMaus.java` 中集成

### RAG 功能扩展
1. 在 `rag/` 包下添加新的组件
2. 配置向量存储和文档处理
3. 更新相关配置类

## 测试

运行测试用例：
```bash
# 运行所有测试
mvn test

# 运行特定测试类
mvn test -Dtest=XiaoyiMausTest
```

## 部署

### 本地部署
```bash
mvn clean package
java -jar target/test1-0.0.1-SNAPSHOT.jar
```

### Docker 部署
```bash
# 构建镜像
docker build -t test1 .

# 运行容器
docker run -p 8080:8080 test1
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 [许可证名称] 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目维护者: [维护者姓名]
- 邮箱: [邮箱地址]
- 项目地址: [项目地址]

## 更新日志

### v1.0.0
- 初始版本发布
- 基础 AI Agent 功能
- RAG 检索增强生成
- 多种工具集成

---

*最后更新时间: 2025年*
