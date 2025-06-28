# frpcStart_en.ps1 - FRP Client Start and Management Script (English Version)
param(
    [string]$Action = "start",
    [string]$ConfigFile = "frpc.toml"
)

# Get script directory
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$FrpcPath = Join-Path $ScriptPath "frpc.exe"
$ConfigPath = Join-Path $ScriptPath $ConfigFile

# Create logs directory
$LogsDir = Join-Path $ScriptPath "logs"
if (-not (Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
}

# Generate timestamped log filename
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LogFileName = "frpc_$Timestamp.log"
$LogPath = Join-Path $LogsDir $LogFileName

# Function to get latest log path
function Get-LatestLogPath {
    if (-not (Test-Path $LogsDir)) {
        New-Item -ItemType Directory -Path $LogsDir -Force | Out-Null
    }
    
    $LatestLog = Get-ChildItem -Path $LogsDir -Filter "frpc_*.log" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($LatestLog) {
        return $LatestLog.FullName
    }
    return $null
}

# Check if frpc.exe exists
if (-not (Test-Path $FrpcPath)) {
    Write-Host "ERROR: frpc.exe not found" -ForegroundColor Red
    exit 1
}

# Check if config file exists
if (-not (Test-Path $ConfigPath)) {
    Write-Host "ERROR: Config file $ConfigFile not found" -ForegroundColor Red
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
    
    $UseLogPath = if ($CustomLogPath) { $CustomLogPath } else { $LogPath }
    
    Add-Content -Path $UseLogPath -Value $LogEntry -Encoding UTF8
    
    if ($Level -eq "ERROR") {
        Add-Content -Path "${UseLogPath}.err" -Value $LogEntry -Encoding UTF8
    }
}

function Start-Frpc {
    Write-Host "Starting FRP Client..." -ForegroundColor Green
    Write-Host "Config: $ConfigPath" -ForegroundColor Yellow
    Write-Host "Log: $LogPath" -ForegroundColor Yellow
    
    Write-LogEntry "Starting FRP Client" "INFO"
    Write-LogEntry "Config file: $ConfigPath" "INFO"
    
    # Check if already running
    $existing = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
    if ($existing) {
        $message = "FRP Client already running (PID: $($existing.Id))"
        Write-Host $message -ForegroundColor Yellow
        Write-LogEntry $message "WARN"
        return
    }
    
    # Start frpc and redirect output to log files
    $TempLogPath = "${LogPath}.temp"
    $TempErrPath = "${LogPath}.temp.err"
    
    $process = Start-Process -FilePath $FrpcPath -ArgumentList "-c", $ConfigPath -RedirectStandardOutput $TempLogPath -RedirectStandardError $TempErrPath -PassThru -WindowStyle Hidden
    
    # Start background job to process log files and clean ANSI codes
    if ($process) {
        $job = Start-Job -ScriptBlock {
            param($TempLog, $FinalLog, $TempErr, $FinalErr)
            
            function Remove-AnsiCodes {
                param([string]$Text)
                return $Text -replace '\x1B\[[0-9;]*[mK]', '' -replace '\[[\d;]*m', ''
            }
            
            # Process standard output (only when process finishes to avoid duplicates)
            if (Test-Path $TempLog) {
                while ($true) {
                    Start-Sleep -Seconds 1
                    
                    # Check if process is still running
                    $runningProcess = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
                    if (-not $runningProcess) {
                        # Process has ended, now process the log file once
                        Start-Sleep -Seconds 2  # Wait for final output
                        try {
                            $finalContent = Get-Content $TempLog -Raw -ErrorAction SilentlyContinue
                            if ($finalContent) {
                                $cleanFinalContent = Remove-AnsiCodes $finalContent
                                Set-Content -Path $FinalLog -Value $cleanFinalContent -Encoding UTF8
                            }
                        } catch {
                            # Ignore errors
                        }
                        break
                    }
                }
            }
            
            # Process error output
            if (Test-Path $TempErr) {
                try {
                    $errorContent = Get-Content $TempErr -Raw -ErrorAction SilentlyContinue
                    if ($errorContent) {
                        $cleanErrorContent = Remove-AnsiCodes $errorContent
                        Set-Content -Path $FinalErr -Value $cleanErrorContent -Encoding UTF8
                    }
                } catch {
                    # Ignore errors
                }
            }
            
            # Clean up temp files
            Remove-Item $TempLog -ErrorAction SilentlyContinue
            Remove-Item $TempErr -ErrorAction SilentlyContinue
            
        } -ArgumentList $TempLogPath, $LogPath, $TempErrPath, "${LogPath}.err"
        
        # Wait briefly for background task to start
        Start-Sleep -Seconds 1
        Write-Host "Background log processing task started (Job ID: $($job.Id))" -ForegroundColor Gray
        Write-Host "Log cleaning will occur when frpc process ends" -ForegroundColor Gray
    }
    
    if ($process) {
        $message = "FRP Client started (PID: $($process.Id))"
        Write-Host $message -ForegroundColor Green
        Write-Host "Standard log: $LogPath" -ForegroundColor Cyan
        Write-Host "Error log: ${LogPath}.err" -ForegroundColor Cyan
        Write-LogEntry $message "INFO"
        Write-LogEntry "Process started successfully, logging frpc output" "INFO"
    } else {
        $message = "Failed to start"
        Write-Host $message -ForegroundColor Red
        Write-LogEntry $message "ERROR"
    }
    
    return
}

function Stop-Frpc {
    Write-Host "Stopping FRP Client..." -ForegroundColor Yellow
    
    $processes = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
    
    if ($processes) {
        foreach ($proc in $processes) {
            Write-Host "Stopping process PID: $($proc.Id)" -ForegroundColor Yellow
            Stop-Process -Id $proc.Id -Force
        }
        Write-Host "FRP Client stopped" -ForegroundColor Green
        
        Start-Sleep -Seconds 3
        
        # Clean up any remaining temp files after stopping
        Write-Host "Cleaning up temporary log files..." -ForegroundColor Gray
        $TempFiles = Get-ChildItem -Path $LogsDir -Filter "*.temp*" -ErrorAction SilentlyContinue
        foreach ($TempFile in $TempFiles) {
            try {
                # Get the corresponding final log file
                $FinalLogPath = $TempFile.FullName -replace '\.temp.*$', ''
                
                # If it's a .temp file (not .temp.err), process the content
                if ($TempFile.Name -match '\.temp$') {
                    if (Test-Path $TempFile.FullName) {
                        $content = Get-Content $TempFile.FullName -Raw -ErrorAction SilentlyContinue
                        if ($content) {
                            # Clean ANSI codes
                            $cleanContent = $content -replace '\x1B\[[0-9;]*[mK]', '' -replace '\[[\d;]*m', ''
                            # Append to final log if it exists, otherwise create new
                            if (Test-Path $FinalLogPath) {
                                Add-Content -Path $FinalLogPath -Value $cleanContent -Encoding UTF8
                            } else {
                                Set-Content -Path $FinalLogPath -Value $cleanContent -Encoding UTF8
                            }
                            Write-Host "  Processed: $($TempFile.Name)" -ForegroundColor Green
                        }
                        Remove-Item $TempFile.FullName -Force -ErrorAction SilentlyContinue
                    }
                } else {
                    # For .temp.err files, just remove them
                    Remove-Item $TempFile.FullName -Force -ErrorAction SilentlyContinue
                    Write-Host "  Removed: $($TempFile.Name)" -ForegroundColor Yellow
                }
            } catch {
                Write-Host "  Failed to process: $($TempFile.Name) - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        
        $CurrentLogPath = Get-LatestLogPath
        if ($CurrentLogPath -and (Test-Path $CurrentLogPath)) {
            foreach ($proc in $processes) {
                $message = "Stopped process PID: $($proc.Id), Start time: $($proc.StartTime)"
                Write-LogEntry $message "INFO" $CurrentLogPath
            }
            Write-LogEntry "FRP Client stopped" "INFO" $CurrentLogPath
        } else {
            $StopLogPath = Join-Path $LogsDir "frpc_stop_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
            Write-LogEntry "Starting to stop FRP Client" "INFO" $StopLogPath
            foreach ($proc in $processes) {
                $message = "Stopped process PID: $($proc.Id), Start time: $($proc.StartTime)"
                Write-LogEntry $message "INFO" $StopLogPath
            }
            Write-LogEntry "FRP Client stopped" "INFO" $StopLogPath
            Write-Host "Stop info logged to: $StopLogPath" -ForegroundColor Cyan
        }
    } else {
        $message = "No running FRP Client process found"
        Write-Host $message -ForegroundColor Yellow
        
        $CurrentLogPath = Get-LatestLogPath
        if ($CurrentLogPath -and (Test-Path $CurrentLogPath)) {
            Write-LogEntry $message "WARN" $CurrentLogPath
        } else {
            $StopLogPath = Join-Path $LogsDir "frpc_stop_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
            Write-LogEntry $message "WARN" $StopLogPath
            Write-Host "Stop info logged to: $StopLogPath" -ForegroundColor Cyan
        }
    }
}

function Show-Status {
    $processes = Get-Process -Name "frpc" -ErrorAction SilentlyContinue
    if ($processes) {
        Write-Host "FRP Client Status: Running" -ForegroundColor Green
        foreach ($proc in $processes) {
            Write-Host "  PID: $($proc.Id), Start time: $($proc.StartTime)" -ForegroundColor Cyan
        }
    } else {
        Write-Host "FRP Client Status: Not running" -ForegroundColor Red
    }
}

function Show-Log {
    param([int]$Lines = 20)
    
    $LatestLog = Get-ChildItem -Path $LogsDir -Filter "frpc_*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    
    if ($LatestLog) {
        $LatestLogPath = $LatestLog.FullName
        $LatestErrorLogPath = "${LatestLogPath}.err"
        
        Write-Host "Showing latest log file: $($LatestLog.Name)" -ForegroundColor Cyan
        Write-Host "Latest $Lines lines of standard output log:" -ForegroundColor Cyan
        if (Test-Path $LatestLogPath) {
            Get-Content $LatestLogPath -Tail $Lines
        } else {
            Write-Host "Log file does not exist" -ForegroundColor Yellow
        }
        
        if (Test-Path $LatestErrorLogPath) {
            Write-Host "`nLatest $Lines lines of error log:" -ForegroundColor Red
            Get-Content $LatestErrorLogPath -Tail $Lines
        } else {
            Write-Host "`nNo error log" -ForegroundColor Green
        }
    } else {
        Write-Host "No log files found" -ForegroundColor Yellow
    }
    
    $AllLogs = Get-ChildItem -Path $LogsDir -Filter "frpc_*.log" | Sort-Object LastWriteTime -Descending
    if ($AllLogs.Count -gt 1) {
        Write-Host "`nAll log files:" -ForegroundColor Cyan
        foreach ($log in $AllLogs) {
            $size = [math]::Round($log.Length / 1KB, 2)
            Write-Host "  $($log.Name) ($($size)KB) - $($log.LastWriteTime)" -ForegroundColor Gray
        }
    }
}

# Main program logic
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
        Write-Host "Usage: .\frpcStart_en.ps1 -Action <start|stop|restart|status|log>" -ForegroundColor Yellow
        Write-Host "  start   - Start frpc" -ForegroundColor Green
        Write-Host "  stop    - Stop frpc" -ForegroundColor Red
        Write-Host "  restart - Restart frpc" -ForegroundColor Blue
        Write-Host "  status  - Show status" -ForegroundColor Cyan
        Write-Host "  log     - Show logs" -ForegroundColor Magenta
    }
} 