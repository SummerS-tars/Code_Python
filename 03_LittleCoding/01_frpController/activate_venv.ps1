# activate_venv.ps1 - Quick activation script for FRP Controller venv
Write-Host "Activating FRP Controller virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host "You can now run: python FRPController.py" -ForegroundColor Cyan
