# frpcStart.ps1 - FRP客户端启动和管理脚本
param(
    [string]$Action = "start",
    [string]$ConfigFile = "frpc.toml"
)

# 获取脚本所在目录
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$FrpcPath = Join-Path $ScriptPath "frpc.exe"
$ConfigPath = Join-Path $ScriptPath $ConfigFile

# 创建logs目录
$LogsDir = Join-Path $ScriptPath "logs"
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

# 生成带时间戳的日志文件名（仅在启动时）
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFileName = "frpc_$Timestamp.log"
$LogPath = Join-Path $LogsDir $LogFileName

# 查找最新日志文件的函数
function Get-LatestLogPath {
    # 确保日志目录存在
    if (-not (Test-Path $LogsDir)) {
        New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
    }
    
    $LatestLog = Get-ChildItem -Path $LogsDir -Filter "frpc_*.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($LatestLog) {
        return $LatestLog.FullName
    }
    return $null
}

# 检查frpc.exe是否存在
if (-not (Test-Path $FrpcPath)) {
    Write-Host "错误: 找不到 frpc.exe 文件" -ForegroundColor Red
    exit 1
}

# 检查配置文件是否存在
if (-not (Test-Path $ConfigPath)) {
    Write-Host "错误: 找不到配置文件 $ConfigFile" -ForegroundColor Red
    exit 1
}

function Write-LogEntry {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [string]$CustomLogPath = $null
    )
    
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    
    # 确定使用哪个日志文件
    $UseLogPath = if ($CustomLogPath) { $CustomLogPath } else { $LogPath }
    
    # 写入标准日志
    Add-Content -Path $UseLogPath -Value $LogEntry -Encoding UTF8
    
    # 如果是错误级别，也写入错误日志
    if ($Level -eq "ERROR") {
        Add-Content -Path "${UseLogPath}.err" -Value $LogEntry -Encoding UTF8
    }
}

function Start-Frpc {
    Write-Host "启动 FRP 客户端..." -ForegroundColor Green
    Write-Host "配置文件: $ConfigPath" -ForegroundColor Yellow
    Write-Host "日志文件: $LogPath" -ForegroundColor Yellow
    
    # 写入启动日志
    Write-LogEntry "开始启动 FRP 客户端" "INFO"
    Write-LogEntry "配置文件: $ConfigPath" "INFO"
    
    # 检查是否已经运行
    $existing = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
    if ($existing) {
        $message = "FRP 客户端已在运行中 (PID: $($existing.Id))"
        Write-Host $message -ForegroundColor Yellow
        Write-LogEntry $message "WARN"
        return
    }
    
    # 启动frpc并重定向输出到日志文件
    # 使用临时文件先捕获输出，然后处理ANSI代码
    $TempLogPath = "${LogPath}.temp"
    $TempErrPath = "${LogPath}.temp.err"
    
    $process = Start-Process -FilePath $FrpcPath -ArgumentList "-c", $ConfigPath -RedirectStandardOutput $TempLogPath -RedirectStandardError $TempErrPath -PassThru -WindowStyle Hidden
    
    # 启动后台任务来处理日志文件，清理ANSI代码
    if ($process) {
        $job = Start-Job -ScriptBlock {
            param($TempLog, $FinalLog, $TempErr, $FinalErr)
            
            function Remove-AnsiCodes {
                param([string]$Text)
                # 移除ANSI转义序列
                return $Text -replace '\x1B\[[0-9;]*[mK]', '' -replace '\[[\d;]*m', ''
            }
            
            # 处理标准输出
            if (Test-Path $TempLog) {
                while ($true) {
                    Start-Sleep -Milliseconds 500
                    try {
                        $content = Get-Content $TempLog -Raw -ErrorAction SilentlyContinue
                        if ($content) {
                            $cleanContent = Remove-AnsiCodes $content
                            Set-Content -Path $FinalLog -Value $cleanContent -Encoding UTF8
                        }
                    } catch {
                        # 文件可能被占用，继续尝试
                    }
                    
                    # 检查进程是否还在运行
                    $runningProcess = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
                    if (-not $runningProcess) {
                        Start-Sleep -Seconds 2  # 等待最后的输出
                        try {
                            $finalContent = Get-Content $TempLog -Raw -ErrorAction SilentlyContinue
                            if ($finalContent) {
                                $cleanFinalContent = Remove-AnsiCodes $finalContent
                                Set-Content -Path $FinalLog -Value $cleanFinalContent -Encoding UTF8
                            }
                        } catch {
                            # 忽略错误
                        }
                        break
                    }
                }
            }
            
            # 处理错误输出
            if (Test-Path $TempErr) {
                try {
                    $errorContent = Get-Content $TempErr -Raw -ErrorAction SilentlyContinue
                    if ($errorContent) {
                        $cleanErrorContent = Remove-AnsiCodes $errorContent
                        Set-Content -Path $FinalErr -Value $cleanErrorContent -Encoding UTF8
                    }
                } catch {
                    # 忽略错误
                }
            }
            
            # 清理临时文件
            Remove-Item $TempLog -ErrorAction SilentlyContinue
            Remove-Item $TempErr -ErrorAction SilentlyContinue
            
        } -ArgumentList $TempLogPath, $LogPath, $TempErrPath, "${LogPath}.err"
        
        # 让后台任务自行运行，不等待
        Write-Host "后台日志处理任务已启动 (Job ID: $($job.Id))" -ForegroundColor Gray
    }
    
    if ($process) {
        $message = "FRP 客户端已启动 (PID: $($process.Id))"
        Write-Host $message -ForegroundColor Green
        Write-Host "标准输出日志: $LogPath" -ForegroundColor Cyan
        Write-Host "错误日志: ${LogPath}.err" -ForegroundColor Cyan
        Write-LogEntry $message "INFO"
        Write-LogEntry "进程启动成功，开始记录frpc输出" "INFO"
    } else {
        $message = "启动失败"
        Write-Host $message -ForegroundColor Red
        Write-LogEntry $message "ERROR"
    }
    
    # 确保函数退出，避免脚本挂起
    return
}

function Stop-Frpc {
    Write-Host "停止 FRP 客户端..." -ForegroundColor Yellow
    
    # 先停止进程，避免与后台作业冲突
    $processes = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
    
    if ($processes) {
        foreach ($proc in $processes) {
            Write-Host "停止进程 PID: $($proc.Id)" -ForegroundColor Yellow
            Stop-Process -Id $proc.Id -Force
        }
        Write-Host "FRP 客户端已停止" -ForegroundColor Green
        
        # 等待后台作业完成清理
        Start-Sleep -Seconds 3
        
        # 然后记录停止信息到日志
        $CurrentLogPath = Get-LatestLogPath
        if ($CurrentLogPath -and (Test-Path $CurrentLogPath)) {
            foreach ($proc in $processes) {
                $message = "停止进程 PID: $($proc.Id), 启动时间: $($proc.StartTime)"
                Write-LogEntry $message "INFO" $CurrentLogPath
            }
            Write-LogEntry "FRP 客户端已停止" "INFO" $CurrentLogPath
        } else {
            # 如果找不到日志文件，创建一个停止记录文件
            $StopLogPath = Join-Path $LogsDir "frpc_stop_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
            Write-LogEntry "开始停止 FRP 客户端" "INFO" $StopLogPath
            foreach ($proc in $processes) {
                $message = "停止进程 PID: $($proc.Id), 启动时间: $($proc.StartTime)"
                Write-LogEntry $message "INFO" $StopLogPath
            }
            Write-LogEntry "FRP 客户端已停止" "INFO" $StopLogPath
            Write-Host "停止信息已记录到: $StopLogPath" -ForegroundColor Cyan
        }
    } else {
        $message = "未找到运行中的 FRP 客户端进程"
        Write-Host $message -ForegroundColor Yellow
        
        # 记录未找到进程的信息
        $CurrentLogPath = Get-LatestLogPath
        if ($CurrentLogPath -and (Test-Path $CurrentLogPath)) {
            Write-LogEntry $message "WARN" $CurrentLogPath
        } else {
            $StopLogPath = Join-Path $LogsDir "frpc_stop_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
            Write-LogEntry $message "WARN" $StopLogPath
            Write-Host "停止信息已记录到: $StopLogPath" -ForegroundColor Cyan
        }
    }
}

function Show-Status {
    $processes = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
    if ($processes) {
        Write-Host "FRP 客户端状态: 运行中" -ForegroundColor Green
        foreach ($proc in $processes) {
            Write-Host "  PID: $($proc.Id), 启动时间: $($proc.StartTime)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "FRP 客户端状态: 未运行" -ForegroundColor Red
    }
}

function Show-Log {
    param([int]$Lines = 20)
    
    # 查找最新的日志文件
    $LatestLog = Get-ChildItem -Path $LogsDir -Filter "frpc_*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($LatestLog) {
        $LatestLogPath = $LatestLog.FullName
        $LatestErrorLogPath = "${LatestLogPath}.err"
        
        Write-Host "显示最新日志文件: $($LatestLog.Name)" -ForegroundColor Cyan
        Write-Host "最新 $Lines 行标准输出日志:" -ForegroundColor Cyan
        if (Test-Path $LatestLogPath) {
            Get-Content $LatestLogPath -Tail $Lines
        } else {
            Write-Host "日志文件不存在" -ForegroundColor Yellow
        }
        
        if (Test-Path $LatestErrorLogPath) {
            Write-Host "`n最新 $Lines 行错误日志:" -ForegroundColor Red
            Get-Content $LatestErrorLogPath -Tail $Lines
        } else {
            Write-Host "`n暂无错误日志" -ForegroundColor Green
        }
    } else {
        Write-Host "未找到任何日志文件" -ForegroundColor Yellow
    }
    
    # 列出所有日志文件
    $AllLogs = Get-ChildItem -Path $LogsDir -Filter "frpc_*.log" | Sort-Object LastWriteTime -Descending
    if ($AllLogs.Count -gt 1) {
        Write-Host "`n所有日志文件:" -ForegroundColor Cyan
        foreach ($log in $AllLogs) {
            $size = [math]::Round($log.Length / 1KB, 2)
            Write-Host "  $($log.Name) ($($size)KB) - $($log.LastWriteTime)" -ForegroundColor Gray
        }
    }
}

# 主程序逻辑
switch ($Action.ToLower()) {
    "start" { Start-Frpc }
    "stop" { Stop-Frpc }
    "restart" { 
        Stop-Frpc
        Start-Sleep -Seconds 2
        Start-Frpc
    }
    "status" { Show-Status }
    "log" { Show-Log }
    default {
        Write-Host "用法: .\frpcStart.ps1 -Action <start|stop|restart|status|log>" -ForegroundColor Yellow
        Write-Host "  start   - 启动 frpc" -ForegroundColor Green
        Write-Host "  stop    - 停止 frpc" -ForegroundColor Red
        Write-Host "  restart - 重启 frpc" -ForegroundColor Blue
        Write-Host "  status  - 显示状态" -ForegroundColor Cyan
        Write-Host "  log     - 显示日志" -ForegroundColor Magenta
    }
} 