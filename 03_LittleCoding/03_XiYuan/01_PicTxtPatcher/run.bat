@echo off
chcp 65001 >nul
echo ==========================================
echo 图片与参数文件匹配处理脚本
echo ==========================================
echo.

echo 请确保你已经正确设置了 pic_txt_patcher.py 中的 base_path 变量
echo.

echo 选择操作:
echo 1. 运行图片与参数文件匹配处理
echo 2. 创建演示测试数据
echo 3. 运行单元测试
echo 4. 退出
echo.

set /p choice="请输入选择 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 正在运行图片与参数文件匹配处理...
    python pic_txt_patcher.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo 正在创建演示测试数据...
    python test_pic_txt_patcher.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo 正在运行单元测试...
    python test_pic_txt_patcher.py
    pause
) else if "%choice%"=="4" (
    echo 退出程序
    exit /b 0
) else (
    echo 无效选择，请重新运行脚本
    pause
)