@echo off

python --version >nul 2>&1 || (
    echo Python is not installed.
    echo Please download and install Python from https://www.python.org/downloads/ first
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