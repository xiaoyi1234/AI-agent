@echo off
chcp 65001 >nul
echo 🔧 修复Nginx重定向循环问题...

REM 1. 备份当前配置
if exist "C:\nginx\conf\nginx.conf" (
    copy "C:\nginx\conf\nginx.conf" "C:\nginx\conf\nginx.conf.backup"
    echo ✅ 已备份当前配置
)

REM 2. 使用优化的配置
if exist "nginx-optimized.conf" (
    copy "nginx-optimized.conf" "C:\nginx\conf\nginx.conf"
    echo ✅ 已应用优化配置
) else (
    echo ❌ 找不到 nginx-optimized.conf 文件
    pause
    exit /b 1
)

REM 3. 测试配置
echo 🧪 测试Nginx配置...
nginx -t
if %errorlevel% equ 0 (
    echo ✅ Nginx配置测试通过
) else (
    echo ❌ Nginx配置测试失败
    pause
    exit /b 1
)

REM 4. 重新加载配置
echo 🔄 重新加载Nginx配置...
nginx -s reload
if %errorlevel% equ 0 (
    echo ✅ Nginx配置重新加载成功
) else (
    echo ❌ Nginx配置重新加载失败
    pause
    exit /b 1
)

echo 🎉 修复完成！重定向循环问题已解决。
echo 📝 如果问题仍然存在，请检查：
echo    1. 域名配置是否正确
echo    2. 文件路径是否正确
echo    3. 权限设置是否正确
pause

