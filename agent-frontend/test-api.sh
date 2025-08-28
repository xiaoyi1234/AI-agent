#!/bin/bash

# API连接测试脚本
# 用于验证后端API是否正常工作

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 后端API地址
BACKEND_URL="https://xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com/api"

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

# 测试基本连接
test_basic_connection() {
    log_info "测试基本连接..."
    
    # 测试HTTPS连接
    if curl -s -I --connect-timeout 10 "$BACKEND_URL" > /dev/null 2>&1; then
        log_success "HTTPS连接正常"
        return 0
    else
        log_error "HTTPS连接失败"
        return 1
    fi
}

# 测试API响应
test_api_response() {
    log_info "测试API响应..."
    
    # 发送GET请求测试API
    response=$(curl -s -w "%{http_code}" --connect-timeout 10 "$BACKEND_URL" -o /tmp/api_response.json)
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        log_success "API响应正常 (HTTP $http_code)"
        if [ -f /tmp/api_response.json ]; then
            log_info "响应内容预览:"
            head -c 200 /tmp/api_response.json
            echo "..."
        fi
        return 0
    else
        log_warning "API响应异常 (HTTP $http_code)"
        if [ -f /tmp/api_response.json ]; then
            log_info "错误响应内容:"
            cat /tmp/api_response.json
        fi
        return 1
    fi
}

# 测试SSE连接
test_sse_connection() {
    log_info "测试SSE连接..."
    
    # 测试SSE端点（如果存在）
    sse_url="$BACKEND_URL/stream/test"
    
    if curl -s -I --connect-timeout 10 "$sse_url" > /dev/null 2>&1; then
        log_success "SSE连接正常"
        return 0
    else
        log_warning "SSE连接测试失败（可能端点不存在）"
        return 1
    fi
}

# 测试CORS设置
test_cors() {
    log_info "测试CORS设置..."
    
    # 发送OPTIONS请求测试CORS
    cors_response=$(curl -s -I -X OPTIONS --connect-timeout 10 \
        -H "Origin: http://localhost" \
        -H "Access-Control-Request-Method: POST" \
        -H "Access-Control-Request-Headers: Content-Type" \
        "$BACKEND_URL" 2>/dev/null)
    
    if echo "$cors_response" | grep -q "Access-Control-Allow-Origin"; then
        log_success "CORS配置正常"
        echo "$cors_response" | grep -E "(Access-Control-Allow-Origin|Access-Control-Allow-Methods|Access-Control-Allow-Headers)"
        return 0
    else
        log_warning "CORS配置可能有问题"
        return 1
    fi
}

# 测试网络延迟
test_latency() {
    log_info "测试网络延迟..."
    
    # 测试连接延迟
    latency=$(curl -s -w "%{time_total}" --connect-timeout 10 "$BACKEND_URL" -o /dev/null)
    
    if (( $(echo "$latency < 5.0" | bc -l) )); then
        log_success "网络延迟正常: ${latency}s"
        return 0
    else
        log_warning "网络延迟较高: ${latency}s"
        return 1
    fi
}

# 测试DNS解析
test_dns() {
    log_info "测试DNS解析..."
    
    domain="xiaoyi-agent-backend-182025-6-1375474591.sh.run.tcloudbase.com"
    
    if nslookup "$domain" > /dev/null 2>&1; then
        log_success "DNS解析正常"
        return 0
    else
        log_error "DNS解析失败"
        return 1
    fi
}

# 主测试函数
main() {
    echo "=========================================="
    echo "    AI技术平台后端API连接测试"
    echo "=========================================="
    echo "后端地址: $BACKEND_URL"
    echo "测试时间: $(date)"
    echo "=========================================="
    
    local total_tests=0
    local passed_tests=0
    
    # 运行所有测试
    tests=(
        "test_dns"
        "test_basic_connection"
        "test_api_response"
        "test_sse_connection"
        "test_cors"
        "test_latency"
    )
    
    for test in "${tests[@]}"; do
        total_tests=$((total_tests + 1))
        if $test; then
            passed_tests=$((passed_tests + 1))
        fi
        echo ""
    done
    
    # 输出测试结果
    echo "=========================================="
    echo "测试结果汇总:"
    echo "总测试数: $total_tests"
    echo "通过测试: $passed_tests"
    echo "失败测试: $((total_tests - passed_tests))"
    
    if [ $passed_tests -eq $total_tests ]; then
        log_success "所有测试通过！API连接正常。"
        exit 0
    else
        log_warning "部分测试失败，请检查配置。"
        exit 1
    fi
}

# 清理临时文件
cleanup() {
    rm -f /tmp/api_response.json
}

# 设置退出时清理
trap cleanup EXIT

# 检查依赖
if ! command -v curl &> /dev/null; then
    log_error "curl 未安装，请先安装 curl"
    exit 1
fi

if ! command -v bc &> /dev/null; then
    log_error "bc 未安装，请先安装 bc"
    exit 1
fi

# 运行测试
main "$@"
