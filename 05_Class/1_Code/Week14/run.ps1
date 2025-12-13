# Week 14 Lab 13 - 天气爬虫启动脚本
# 用于快速启动程序

Write-Host "================================" -ForegroundColor Cyan
Write-Host "🌤️  天气查询爬虫系统" -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python 是否安装
try {
    $pythonCmd = "E:/_ComputerLearning/7_Programming_Python/Code_Python/venv/Scripts/python.exe"
    
    if (Test-Path $pythonCmd) {
        Write-Host "✅ Python 环境已找到" -ForegroundColor Green
    } else {
        Write-Host "❌ 未找到 Python 虚拟环境" -ForegroundColor Red
        exit 1
    }
    
    # 检查 requests 库
    Write-Host "🔍 检查依赖..." -ForegroundColor Yellow
    & $pythonCmd -c "import requests" 2>$null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 依赖库已安装" -ForegroundColor Green
    } else {
        Write-Host "⚠️  正在安装依赖..." -ForegroundColor Yellow
        & $pythonCmd -m pip install requests
    }
    
    Write-Host ""
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "启动程序..." -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    
    # 运行主程序
    & $pythonCmd weather_crawler.py
    
} catch {
    Write-Host "❌ 运行出错: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
