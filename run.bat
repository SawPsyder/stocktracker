@echo off

python --version >nul 2>&1 || (
    echo Python is not installed.
    echo Please install it first. You can use the Microsoft Store for that.
    call python
    pause
    exit /b 1
)

reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1 || (
    echo Google Chrome is not installed.
    echo Please download and install Google Chrome from https://www.google.com/chrome/ first
    pause
    exit /b 1
)

if not exist .venv (
    call install.bat --no-pause
)

echo Activating virtual environment...
call .venv\Scripts\activate

echo Running the program...
python main.py

echo Deactivating virtual environment...
call .venv\Scripts\deactivate

echo Program finished.
echo.
pause