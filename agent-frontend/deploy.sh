#!/bin/bash

# AI技术平台前端部署脚本
# 使用方法: ./deploy.sh [production|staging]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    if ! command -v node &> /dev/null; then
        log_error "Node.js 未安装"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        log_error "npm 未安装"
        exit 1
    fi
    
    log_success "依赖检查完成"
}

# 安装依赖
install_dependencies() {
    log_info "安装项目依赖..."
    npm install
    log_success "依赖安装完成"
}

# 构建项目
build_project() {
    local env=${1:-production}
    log_info "构建项目 (环境: $env)..."
    
    if [ "$env" = "production" ]; then
        npm run build
    else
        # 开发环境构建
        npm run build -- --mode development
    fi
    
    log_success "项目构建完成"
}

# 检查构建结果
check_build() {
    log_info "检查构建结果..."
    
    if [ ! -d "dist" ]; then
        log_error "构建失败: dist 目录不存在"
        exit 1
    fi
    
    if [ ! -f "dist/index.html" ]; then
        log_error "构建失败: index.html 不存在"
        exit 1
    fi
    
    log_success "构建结果检查完成"
}

# 部署到服务器（示例）
deploy_to_server() {
    local env=${1:-production}
    log_info "部署到服务器 (环境: $env)..."
    
    # 这里需要根据实际情况配置
    # 示例：使用rsync部署到远程服务器
    # rsync -avz --delete dist/ user@server:/var/www/agent-frontend/
    
    # 示例：使用scp部署
    # scp -r dist/* user@server:/var/www/agent-frontend/
    
    log_warning "请根据实际情况配置部署命令"
    log_info "构建文件位于 dist/ 目录"
    log_info "请手动将 dist/ 目录内容复制到服务器的 /var/www/agent-frontend/ 目录"
}

# 重启nginx
restart_nginx() {
    log_info "重启nginx..."
    
    # 检查nginx配置
    if command -v nginx &> /dev/null; then
        nginx -t
        if [ $? -eq 0 ]; then
            systemctl reload nginx || systemctl restart nginx
            log_success "nginx重启完成"
        else
            log_error "nginx配置检查失败"
            exit 1
        fi
    else
        log_warning "nginx未安装或不在PATH中"
    fi
}

# 主函数
main() {
    local env=${1:-production}
    
    log_info "开始部署 AI技术平台前端 (环境: $env)"
    
    # 检查依赖
    check_dependencies
    
    # 安装依赖
    install_dependencies
    
    # 构建项目
    build_project $env
    
    # 检查构建结果
    check_build
    
    # 部署到服务器
    deploy_to_server $env
    
    # 重启nginx
    restart_nginx
    
    log_success "部署完成！"
    log_info "访问地址: http://your-domain.com"
}

# 脚本入口
if [ "$1" = "help" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "AI技术平台前端部署脚本"
    echo ""
    echo "使用方法:"
    echo "  ./deploy.sh [production|staging]"
    echo ""
    echo "参数:"
    echo "  production  生产环境部署 (默认)"
    echo "  staging     测试环境部署"
    echo ""
    echo "示例:"
    echo "  ./deploy.sh production"
    echo "  ./deploy.sh staging"
    exit 0
fi

# 执行主函数
main "$@"
