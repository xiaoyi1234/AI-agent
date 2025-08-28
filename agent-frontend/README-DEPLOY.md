# AI技术平台前端部署指南

## 项目概述

这是一个基于 Vue 3 + Vite 的前端项目，包含多个AI聊天应用：
- PCIE技术顾问
- AI超级智能体  
- 打字机版聊天

## 部署前准备

### 1. 服务器要求

- **操作系统**: Ubuntu 18.04+ / CentOS 7+ / Debian 9+
- **内存**: 至少 1GB RAM
- **存储**: 至少 2GB 可用空间
- **网络**: 支持 HTTP/HTTPS 访问

### 2. 软件依赖

```bash
# 安装 Node.js 和 npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 安装 nginx
sudo apt-get update
sudo apt-get install -y nginx

# 验证安装
node --version
npm --version
nginx -v
```

## 部署步骤

### 1. 构建前端项目

```bash
# 克隆项目（如果从Git仓库）
git clone <your-repo-url>
cd agent-frontend

# 或者直接使用当前项目目录
cd /path/to/agent-frontend

# 安装依赖
npm install

# 构建项目
npm run build
```

### 2. 配置 Nginx

#### 2.1 复制配置文件

```bash
# 将 nginx.conf 复制到 nginx 配置目录
sudo cp nginx.conf /etc/nginx/sites-available/agent-frontend

# 创建软链接启用站点
sudo ln -s /etc/nginx/sites-available/agent-frontend /etc/nginx/sites-enabled/

# 删除默认站点（可选）
sudo rm /etc/nginx/sites-enabled/default
```

#### 2.2 修改配置

编辑配置文件 `/etc/nginx/sites-available/agent-frontend`：

```bash
sudo nano /etc/nginx/sites-available/agent-frontend
```

**重要修改项：**

1. **服务器名称**：
   ```nginx
   server_name your-domain.com www.your-domain.com;
   ```
   替换为你的实际域名

2. **网站根目录**：
   ```nginx
   root /var/www/agent-frontend/dist;
   ```
   确保路径指向构建后的 dist 目录

3. **后端API地址**（已配置）：
   ```nginx
   proxy_pass https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api/;
   ```

### 3. 部署文件

```bash
# 创建网站目录
sudo mkdir -p /var/www/agent-frontend

# 复制构建文件
sudo cp -r dist/* /var/www/agent-frontend/

# 设置权限
sudo chown -R www-data:www-data /var/www/agent-frontend
sudo chmod -R 755 /var/www/agent-frontend
```

### 4. 测试和启动

```bash
# 测试 nginx 配置
sudo nginx -t

# 如果测试通过，重启 nginx
sudo systemctl restart nginx

# 检查 nginx 状态
sudo systemctl status nginx
```

### 5. 使用部署脚本（可选）

```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh production

# 查看帮助
./deploy.sh help
```

### 6. 测试API连接

```bash
# 给测试脚本执行权限
chmod +x test-api.sh

# 运行API连接测试
./test-api.sh

# 手动测试API
curl -I https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api/
```

## 配置说明

### Nginx 配置特性

1. **API 代理**：
   - 所有 `/api/*` 请求代理到后端服务器
   - 支持 SSE (Server-Sent Events) 流式响应
   - 自动处理 CORS 和请求头

2. **静态资源优化**：
   - 启用 gzip 压缩
   - 设置长期缓存策略
   - 优化图片和字体文件

3. **安全配置**：
   - 添加安全响应头
   - 防止 XSS 和点击劫持
   - 隐藏服务器信息

4. **Vue Router 支持**：
   - 支持 HTML5 History 模式
   - 自动回退到 index.html

### 环境变量配置

如果需要配置不同环境的API地址，可以修改 `src/utils/chat.js`：

```javascript
// 根据环境设置不同的 baseURL
const baseURL = process.env.NODE_ENV === 'production' 
  ? '/api'  // 生产环境使用相对路径，由nginx代理
  : 'http://localhost:8888';  // 开发环境直接访问

export const apiClient = axios.create({
  baseURL: baseURL,
  timeout: 30000
})
```

## HTTPS 配置（推荐）

### 1. 获取 SSL 证书

使用 Let's Encrypt 免费证书：

```bash
# 安装 certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo crontab -e
# 添加：0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. 启用 HTTPS 配置

取消注释 `nginx.conf` 中的 HTTPS 配置部分，并修改域名和证书路径。

## 监控和维护

### 1. 日志查看

```bash
# 查看 nginx 访问日志
sudo tail -f /var/log/nginx/access.log

# 查看 nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# 查看系统日志
sudo journalctl -u nginx -f
```

### 2. 性能监控

```bash
# 检查 nginx 状态
sudo nginx -t

# 查看 nginx 进程
ps aux | grep nginx

# 检查端口占用
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443
```

### 3. 备份和恢复

```bash
# 备份配置文件
sudo cp /etc/nginx/sites-available/agent-frontend /backup/nginx-agent-frontend.conf

# 备份网站文件
sudo cp -r /var/www/agent-frontend /backup/agent-frontend-$(date +%Y%m%d)
```

## 故障排除

### 常见问题

1. **502 Bad Gateway**：
   - 检查后端服务是否正常运行
   - 验证 API 地址是否正确
   - 检查防火墙设置

2. **404 Not Found**：
   - 确认 dist 目录文件已正确部署
   - 检查 nginx 配置中的 root 路径
   - 验证文件权限

3. **CORS 错误**：
   - 检查 nginx 代理配置
   - 确认后端 CORS 设置

4. **SSE 连接失败**：
   - 检查 `/api/stream/` 代理配置
   - 确认后端支持 SSE

### 调试命令

```bash
# 检查 nginx 配置语法
sudo nginx -t

# 重新加载配置
sudo nginx -s reload

# 查看 nginx 版本和编译信息
nginx -V

# 测试 API 连接
curl -I https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api/

# 使用测试脚本
chmod +x test-api.sh
./test-api.sh
```

## 更新部署

### 1. 代码更新

```bash
# 拉取最新代码
git pull origin main

# 重新构建
npm run build

# 部署新文件
sudo cp -r dist/* /var/www/agent-frontend/

# 重启 nginx
sudo systemctl reload nginx
```

### 2. 配置更新

```bash
# 备份当前配置
sudo cp /etc/nginx/sites-available/agent-frontend /backup/

# 更新配置
sudo nano /etc/nginx/sites-available/agent-frontend

# 测试并重启
sudo nginx -t && sudo systemctl reload nginx
```

## 联系支持

如果在部署过程中遇到问题，请检查：
1. 服务器日志
2. nginx 错误日志
3. 浏览器开发者工具的网络和控制台

确保所有配置都正确设置，特别是域名和API地址。
