# setup_venv.ps1 - Virtual Environment Setup Script for FRP Controller
param(
    [string]$VenvName = "venv",
    [switch]$Force
)

Write-Host "FRP Controller - Virtual Environment Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Get script directory
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
$VenvPath = Join-Path $ScriptPath $VenvName
$RequirementsFile = Join-Path $ScriptPath "requirements.txt"

# Check if Python is available
try {
    $PythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $PythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Error: Python not found in PATH" -ForegroundColor Red
    Write-Host "Please install Python and add it to your PATH" -ForegroundColor Yellow
    exit 1
}

# Check if venv already exists
if (Test-Path $VenvPath) {
    if ($Force) {
        Write-Host "⚠ Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item $VenvPath -Recurse -Force
    } else {
        Write-Host "⚠ Virtual environment already exists at: $VenvPath" -ForegroundColor Yellow
        $choice = Read-Host "Do you want to recreate it? (y/N)"
        if ($choice -eq 'y' -or $choice -eq 'Y') {
            Remove-Item $VenvPath -Recurse -Force
        } else {
            Write-Host "Skipping virtual environment creation" -ForegroundColor Yellow
            # Still try to install/update packages
            $ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
            if (Test-Path $ActivateScript) {
                Write-Host "Using existing virtual environment..." -ForegroundColor Green
                & $ActivateScript
                Write-Host "✓ Virtual environment activated" -ForegroundColor Green
                
                # Install/update packages
                if (Test-Path $RequirementsFile) {
                    Write-Host "Installing/updating packages from requirements.txt..." -ForegroundColor Blue
                    pip install -r $RequirementsFile --upgrade
                    Write-Host "✓ Packages installed/updated successfully" -ForegroundColor Green
                } else {
                    Write-Host "⚠ requirements.txt not found, installing basic dependencies..." -ForegroundColor Yellow
                    pip install toml --upgrade
                    Write-Host "✓ Basic dependencies installed" -ForegroundColor Green
                }
                
                Write-Host "`nSetup completed! To activate the virtual environment in the future, run:" -ForegroundColor Cyan
                Write-Host "  .\$VenvName\Scripts\Activate.ps1" -ForegroundColor White
                Write-Host "Or use the activation script: .\activate_venv.ps1" -ForegroundColor White
                exit 0
            } else {
                Write-Host "✗ Existing virtual environment is corrupted, recreating..." -ForegroundColor Red
                Remove-Item $VenvPath -Recurse -Force
            }
        }
    }
}

# Create virtual environment
Write-Host "Creating virtual environment at: $VenvPath" -ForegroundColor Blue
try {
    python -m venv $VenvPath
    Write-Host "✓ Virtual environment created successfully" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    Write-Host "Activating virtual environment..." -ForegroundColor Blue
    try {
        & $ActivateScript
        Write-Host "✓ Virtual environment activated" -ForegroundColor Green
    } catch {
        Write-Host "⚠ Failed to activate virtual environment automatically" -ForegroundColor Yellow
        Write-Host "You can activate it manually later with: .\$VenvName\Scripts\Activate.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ Activation script not found" -ForegroundColor Red
    exit 1
}

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Blue
try {
    python -m pip install --upgrade pip
    Write-Host "✓ pip upgraded successfully" -ForegroundColor Green
} catch {
    Write-Host "⚠ Failed to upgrade pip, continuing..." -ForegroundColor Yellow
}

# Install dependencies
if (Test-Path $RequirementsFile) {
    Write-Host "Installing packages from requirements.txt..." -ForegroundColor Blue
    try {
        pip install -r $RequirementsFile
        Write-Host "✓ All packages installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install some packages" -ForegroundColor Red
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "You can try installing manually: pip install -r requirements.txt" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ requirements.txt not found, installing basic dependencies..." -ForegroundColor Yellow
    try {
        pip install toml
        Write-Host "✓ Basic dependencies (toml) installed" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install basic dependencies" -ForegroundColor Red
        Write-Host "You can try installing manually: pip install toml" -ForegroundColor Yellow
    }
}

# Verify installation
Write-Host "`nVerifying installation..." -ForegroundColor Blue
try {
    python -c "import toml; print('✓ toml module available')"
    Write-Host "✓ All required modules are available" -ForegroundColor Green
} catch {
    Write-Host "⚠ Some modules may not be properly installed" -ForegroundColor Yellow
}

# Create activation helper script
$ActivationHelper = Join-Path $ScriptPath "activate_venv.ps1"
$HelperContent = @"
# activate_venv.ps1 - Quick activation script for FRP Controller venv
Write-Host "Activating FRP Controller virtual environment..." -ForegroundColor Green
& ".\$VenvName\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host "You can now run: python FRPController.py" -ForegroundColor Cyan
"@

Set-Content -Path $ActivationHelper -Value $HelperContent -Encoding UTF8
Write-Host "✓ Created activation helper: activate_venv.ps1" -ForegroundColor Green

# Summary
Write-Host "`n" + "="*50 -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "="*50 -ForegroundColor Cyan
Write-Host "Virtual environment: $VenvPath" -ForegroundColor White
Write-Host "`nTo use the FRP Controller:" -ForegroundColor Cyan
Write-Host "1. Activate the virtual environment:" -ForegroundColor White
Write-Host "   .\activate_venv.ps1" -ForegroundColor Yellow
Write-Host "2. Run the FRP Controller:" -ForegroundColor White
Write-Host "   python FRPController.py" -ForegroundColor Yellow
Write-Host "`nThe virtual environment is currently activated in this session." -ForegroundColor Green 