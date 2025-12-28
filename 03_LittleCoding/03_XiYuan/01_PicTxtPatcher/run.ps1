# 图片与参数文件匹配处理脚本 - PowerShell启动器
# Author: GitHub Copilot

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "图片与参数文件匹配处理脚本" -ForegroundColor Yellow
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "请确保你已经正确设置了 pic_txt_patcher.py 中的 base_path 变量" -ForegroundColor Red
Write-Host ""

Write-Host "选择操作:" -ForegroundColor Green
Write-Host "1. 运行图片与参数文件匹配处理" -ForegroundColor White
Write-Host "2. 创建演示测试数据" -ForegroundColor White  
Write-Host "3. 运行单元测试" -ForegroundColor White
Write-Host "4. 查看帮助文档" -ForegroundColor White
Write-Host "5. 退出" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请输入选择 (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "正在运行图片与参数文件匹配处理..." -ForegroundColor Yellow
        python pic_txt_patcher.py
        Write-Host ""
        Write-Host "处理完成！请查看生成的日志文件获取详细信息。" -ForegroundColor Green
    }
    "2" {
        Write-Host ""
        Write-Host "正在创建演示测试数据..." -ForegroundColor Yellow
        python test_pic_txt_patcher.py
    }
    "3" {
        Write-Host ""
        Write-Host "正在运行单元测试..." -ForegroundColor Yellow
        python -m unittest test_pic_txt_patcher.TestPicTxtPatcher -v
    }
    "4" {
        Write-Host ""
        Write-Host "打开README.md文档..." -ForegroundColor Yellow
        if (Test-Path "README.md") {
            Start-Process "README.md"
        } else {
            Write-Host "README.md 文件不存在" -ForegroundColor Red
        }
    }
    "5" {
        Write-Host "退出程序" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "无效选择，请重新运行脚本" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "按任意键继续..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")