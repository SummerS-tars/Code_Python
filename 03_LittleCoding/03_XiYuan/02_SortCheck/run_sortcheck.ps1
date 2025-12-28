<#
交互式封装脚本: 便于多次对不同目录执行 sortcheck.py

功能:
 1. 循环读取用户输入的目标目录路径
 2. 支持命令: help / h, quit / q, apply, verbose, last, history, clear
 3. 维护最近输入目录历史 (内存, 会话内有效)
 4. 每次默认 dry-run, 输入 apply 才会对下次执行启用 --apply
 5. 提供 Tab 补全 (依赖用户 shell 默认) - 直接输入路径或拖拽

使用:
  在本目录 PowerShell 中执行:
    pwsh ./run_sortcheck.ps1

可选初始参数:
  -PythonExe <path>    指定 python 解释器
  -ScriptPath <path>   指定 sortcheck.py 路径 (默认同目录)
#>
param(
    [string]$PythonExe = 'python',
    [string]$ScriptPath = (Join-Path $PSScriptRoot 'sortcheck.py')
)

if (-not (Test-Path $ScriptPath)) {
    Write-Host "[ERROR] 找不到 sortcheck.py: $ScriptPath" -ForegroundColor Red
    exit 2
}

Write-Host "==== SortCheck Interactive Runner ====" -ForegroundColor Cyan
Write-Host "输入目录路径以执行检查 (默认 dry-run)" -ForegroundColor DarkCyan
Write-Host "指令: help | apply | verbose | q | history | last | clear" -ForegroundColor DarkCyan

$history = @()
$applyMode = $false  # 持久 apply 开关
$dupInteractiveMode = $false  # 持久 duplicate 交互
$verbose = $false
$classAllMode = $false  # 当为 true 时，输入路径作为 --class-all 根目录

function Show-Help() {
    Write-Host "指令说明 (可用数字或单词):" -ForegroundColor Yellow
    Write-Host " 1 / dir      输入目录路径执行检查 (当前模式: $([bool](-not $classAllMode) -as [string]))"
    Write-Host " 2 / apply    切换是否执行实际重命名 (当前: $applyMode)"
    Write-Host " 3 / fixdup   切换是否进入 duplicate 交互 (当前: $dupInteractiveMode)"
    Write-Host " 4 / verbose  切换 verbose (当前: $verbose)"
    Write-Host " 5 / last     重新运行上次目录"
    Write-Host " 6 / history  查看历史目录"
    Write-Host " 7 / status   查看当前状态"
    Write-Host " 8 / clear    清屏"
    Write-Host " 9 / help     帮助"
    Write-Host " 10 / mode    切换输入路径模式 dir/class_all (当前: $([string]($classAllMode ? 'class_all' : 'dir')))"
    Write-Host " 0 / quit     退出"
}

function Run-SortCheck([string]$pathArg) {
    if (-not (Test-Path $pathArg)) {
        Write-Host "[WARN] 路径不存在: $pathArg" -ForegroundColor Yellow
        return
    }
    $argsList = @($ScriptPath)
    if ($classAllMode) {
        $argsList += @('--class-all', $pathArg)
    }
    else {
        $argsList += @('-d', $pathArg)
    }
    if ($applyMode) { $argsList += '--apply' }
    if ($verbose) { $argsList += '--verbose' }
    if ($dupInteractiveMode) { $argsList += '--interactive-dup' }
    Write-Host "\n>>> 执行: $PythonExe $($argsList -join ' ')" -ForegroundColor Green
    try { & $PythonExe @argsList } catch { Write-Host "[ERROR] 执行失败: $_" -ForegroundColor Red }
}

while ($true) {
    Write-Host ""  # 空行
    Write-Host "===========================" -ForegroundColor DarkGray
    Write-Host "当前状态: apply=$applyMode  dupInteractive=$dupInteractiveMode  verbose=$verbose  历史数=$($history.Count)" -ForegroundColor DarkCyan
    if ($history.Count -gt 0) { Write-Host "上次目录: $($history[-1])" -ForegroundColor DarkCyan }
    Write-Host "菜单: 1=目录 2=apply 3=fixdup 4=verbose 5=last 6=history 7=status 8=clear 9=help 10=mode 0=quit" -ForegroundColor DarkGray
    $rawInput = Read-Host -Prompt '[输入编号/指令/目录路径]'
    $inputText = ($rawInput | ForEach-Object { $_.Trim() })
    if (-not $inputText) { continue }
    $cmdLower = $inputText.ToLower()

    switch ($cmdLower) {
        '0' { break }
        'quit' { break }
        'q' { break }
        '9' { Show-Help; continue }
        'help' { Show-Help; continue }
        '2' { $applyMode = -not $applyMode; Write-Host "applyMode -> $applyMode" -ForegroundColor Magenta; continue }
        'apply' { $applyMode = -not $applyMode; Write-Host "applyMode -> $applyMode" -ForegroundColor Magenta; continue }
        '3' { $dupInteractiveMode = -not $dupInteractiveMode; Write-Host "dupInteractive -> $dupInteractiveMode" -ForegroundColor Magenta; continue }
        'fixdup' { $dupInteractiveMode = -not $dupInteractiveMode; Write-Host "dupInteractive -> $dupInteractiveMode" -ForegroundColor Magenta; continue }
        '4' { $verbose = -not $verbose; Write-Host "verbose -> $verbose" -ForegroundColor Magenta; continue }
        'verbose' { $verbose = -not $verbose; Write-Host "verbose -> $verbose" -ForegroundColor Magenta; continue }
        '5' {
            if ($history.Count -eq 0) { Write-Host "(无 last)"; continue }
            $dir=$history[-1]; Run-SortCheck -dir $dir; continue }
        'last' {
            if ($history.Count -eq 0) { Write-Host "(无 last)"; continue }
            $dir=$history[-1]; Run-SortCheck -dir $dir; continue }
        '6' { if ($history.Count -eq 0) { Write-Host "(无历史)" } else { 0..($history.Count-1) | ForEach-Object { Write-Host "[$_] $($history[$_])" } }; continue }
        'history' { if ($history.Count -eq 0) { Write-Host "(无历史)" } else { 0..($history.Count-1) | ForEach-Object { Write-Host "[$_] $($history[$_])" } }; continue }
        '7' { Write-Host "apply=$applyMode dupInteractive=$dupInteractiveMode verbose=$verbose history=$($history.Count)" -ForegroundColor DarkCyan; if ($history.Count -gt 0){Write-Host "last=$($history[-1])" -ForegroundColor DarkCyan}; continue }
        'status' { Write-Host "apply=$applyMode dupInteractive=$dupInteractiveMode verbose=$verbose history=$($history.Count)" -ForegroundColor DarkCyan; if ($history.Count -gt 0){Write-Host "last=$($history[-1])" -ForegroundColor DarkCyan}; continue }
        '8' { Clear-Host; continue }
        'clear' { Clear-Host; continue }
        '10' { $classAllMode = -not $classAllMode; Write-Host "路径模式 -> $([string]($classAllMode ? 'class_all (递归 pic)' : 'dir'))" -ForegroundColor Magenta; continue }
        'mode' { $classAllMode = -not $classAllMode; Write-Host "路径模式 -> $([string]($classAllMode ? 'class_all (递归 pic)' : 'dir'))" -ForegroundColor Magenta; continue }
        '.' { $current = Get-Location; Run-SortCheck -dir $current.Path; if ($history.Count -eq 0 -or $history[-1] -ne $current.Path) { $history += $current.Path }; continue }
    }

    # 其它输入如果是存在的目录则执行
    if (Test-Path $inputText) {
        $pathArg = $inputText.Trim('"')
        Run-SortCheck -pathArg $pathArg
        if ($pathArg -and -not ($history -and $history[-1] -eq $pathArg)) { $history += $pathArg }
        continue
    }
    Write-Host "[WARN] 未识别的输入: $inputText  (输入 9 或 help 查看菜单)" -ForegroundColor Yellow
}

Write-Host "退出。" -ForegroundColor Cyan
