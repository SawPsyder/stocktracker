@echo off

python --version >nul 2>&1 || (
    echo Python is not installed.
    echo Please install it first. You can use the Microsoft Store for that.
    call python
    pause
    exit /b 1
)

if exist .venv (
    echo Virtual environment already exists. Deleting old virtual environment...
    rmdir /s /q .venv
)

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Deactivating virtual environment...
call .venv\Scripts\deactivate

echo Installation complete.
echo.

if not "%1"=="--no-pause" (
    pause
)