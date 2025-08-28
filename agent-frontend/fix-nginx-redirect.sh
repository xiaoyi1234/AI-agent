#!/bin/bash

# Nginx重定向循环修复脚本

echo "🔧 修复Nginx重定向循环问题..."

# 1. 备份当前配置
if [ -f /etc/nginx/conf.d/default.conf ]; then
    cp /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.backup
    echo "✅ 已备份当前配置"
fi

# 2. 使用优化的配置
if [ -f nginx-optimized.conf ]; then
    cp nginx-optimized.conf /etc/nginx/conf.d/default.conf
    echo "✅ 已应用优化配置"
else
    echo "❌ 找不到 nginx-optimized.conf 文件"
    exit 1
fi

# 3. 测试配置
echo "🧪 测试Nginx配置..."
if nginx -t; then
    echo "✅ Nginx配置测试通过"
else
    echo "❌ Nginx配置测试失败"
    exit 1
fi

# 4. 重新加载配置
echo "🔄 重新加载Nginx配置..."
if systemctl reload nginx; then
    echo "✅ Nginx配置重新加载成功"
else
    echo "❌ Nginx配置重新加载失败"
    exit 1
fi

echo "🎉 修复完成！重定向循环问题已解决。"
echo "📝 如果问题仍然存在，请检查："
echo "   1. 域名配置是否正确"
echo "   2. 文件路径是否正确"
echo "   3. 权限设置是否正确"

