# 地铁换乘路径规划系统 - 快速启动脚本
# PowerShell 脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  地铁换乘路径规划系统" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 切换到src目录
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcPath = Join-Path $scriptPath "src"

if (-not (Test-Path $srcPath)) {
    Write-Host "错误: 找不到src目录" -ForegroundColor Red
    exit 1
}

Set-Location $srcPath

# 检查Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未找到Python，请先安装Python 3.11+" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "选择运行模式:" -ForegroundColor Yellow
Write-Host "  1. 交互式模式（推荐）" -ForegroundColor White
Write-Host "  2. 运行测试用例" -ForegroundColor White
Write-Host "  3. 单次查询" -ForegroundColor White
Write-Host ""

$choice = Read-Host "请输入选择 (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n启动交互式模式..." -ForegroundColor Green
        python main.py
    }
    "2" {
        Write-Host "`n运行测试用例..." -ForegroundColor Green
        python main.py --test
    }
    "3" {
        Write-Host ""
        $query = Read-Host "请输入查询（格式：起始线路，起始站名-目标线路，目标站名）"
        if ($query) {
            Write-Host "`n查询中..." -ForegroundColor Green
            python main.py $query
        } else {
            Write-Host "输入为空，退出" -ForegroundColor Red
        }
    }
    default {
        Write-Host "`n无效选择，启动交互式模式..." -ForegroundColor Yellow
        python main.py
    }
}

Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
