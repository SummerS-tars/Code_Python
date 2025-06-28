@echo off
REM setup_venv.bat - Virtual Environment Setup Script for FRP Controller

echo FRP Controller - Virtual Environment Setup
echo ==========================================

REM Get script directory
set SCRIPT_DIR=%~dp0
set VENV_PATH=%SCRIPT_DIR%venv
set REQUIREMENTS_FILE=%SCRIPT_DIR%requirements.txt

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    echo Please install Python and add it to your PATH
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python found: %PYTHON_VERSION%

REM Check if venv already exists
if exist "%VENV_PATH%" (
    echo [WARNING] Virtual environment already exists at: %VENV_PATH%
    set /p choice="Do you want to recreate it? (y/N): "
    if /i "%choice%"=="y" (
        echo Removing existing virtual environment...
        rmdir /s /q "%VENV_PATH%"
    ) else (
        echo Skipping virtual environment creation
        goto activate_existing
    )
)

REM Create virtual environment
echo Creating virtual environment at: %VENV_PATH%
python -m venv "%VENV_PATH%"
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created successfully

REM Activate virtual environment
echo Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
if errorlevel 1 (
    echo [WARNING] Failed to activate virtual environment automatically
    echo You can activate it manually later with: venv\Scripts\activate.bat
) else (
    echo [OK] Virtual environment activated
)

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [WARNING] Failed to upgrade pip, continuing...
) else (
    echo [OK] pip upgraded successfully
)

REM Install dependencies
if exist "%REQUIREMENTS_FILE%" (
    echo Installing packages from requirements.txt...
    pip install -r "%REQUIREMENTS_FILE%"
    if errorlevel 1 (
        echo [ERROR] Failed to install some packages
        echo You can try installing manually: pip install -r requirements.txt
    ) else (
        echo [OK] All packages installed successfully
    )
) else (
    echo [WARNING] requirements.txt not found, installing basic dependencies...
    pip install toml
    if errorlevel 1 (
        echo [ERROR] Failed to install basic dependencies
        echo You can try installing manually: pip install toml
    ) else (
        echo [OK] Basic dependencies (toml) installed
    )
)

REM Verify installation
echo.
echo Verifying installation...
python -c "import toml; print('[OK] toml module available')" 2>nul
if errorlevel 1 (
    echo [WARNING] Some modules may not be properly installed
) else (
    echo [OK] All required modules are available
)

REM Create activation helper script
echo @echo off > "%SCRIPT_DIR%activate_venv.bat"
echo echo Activating FRP Controller virtual environment... >> "%SCRIPT_DIR%activate_venv.bat"
echo call "%%~dp0venv\Scripts\activate.bat" >> "%SCRIPT_DIR%activate_venv.bat"
echo echo [OK] Virtual environment activated >> "%SCRIPT_DIR%activate_venv.bat"
echo echo You can now run: python FRPController.py >> "%SCRIPT_DIR%activate_venv.bat"
echo cmd /k >> "%SCRIPT_DIR%activate_venv.bat"

echo [OK] Created activation helper: activate_venv.bat

goto summary

:activate_existing
REM Try to activate existing environment
if exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Using existing virtual environment...
    call "%VENV_PATH%\Scripts\activate.bat"
    echo [OK] Virtual environment activated
    
    REM Install/update packages
    if exist "%REQUIREMENTS_FILE%" (
        echo Installing/updating packages from requirements.txt...
        pip install -r "%REQUIREMENTS_FILE%" --upgrade
        echo [OK] Packages installed/updated successfully
    ) else (
        echo [WARNING] requirements.txt not found, installing basic dependencies...
        pip install toml --upgrade
        echo [OK] Basic dependencies installed
    )
    
    echo.
    echo Setup completed! To activate the virtual environment in the future, run:
    echo   activate_venv.bat
    echo Or directly: venv\Scripts\activate.bat
    pause
    exit /b 0
) else (
    echo [ERROR] Existing virtual environment is corrupted, please delete the venv folder and run this script again
    pause
    exit /b 1
)

:summary
echo.
echo ==================================================
echo Setup completed successfully!
echo ==================================================
echo Virtual environment: %VENV_PATH%
echo.
echo To use the FRP Controller:
echo 1. Activate the virtual environment:
echo    activate_venv.bat
echo 2. Run the FRP Controller:
echo    python FRPController.py
echo.
echo The virtual environment is currently activated in this session.
pause 