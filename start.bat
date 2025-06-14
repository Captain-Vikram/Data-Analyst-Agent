<<<<<<< HEAD
@echo off
echo 🤖 AI Data Analyst Agent - Quick Start
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🤖 Setup complete!
echo.
echo Next steps:
echo 1. Make sure LM Studio is running with a model loaded (for local backend)
echo 2. Or set TOGETHER_API_KEY environment variable (for cloud backend)
echo.
echo Press any key to start the application...
pause >nul

python main.py
=======
@echo off
echo 🤖 AI Data Analyst Agent - Quick Start
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Creating virtual environment...
    python -m venv .venv
)

echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🤖 Setup complete!
echo.
echo Next steps:
echo 1. Make sure LM Studio is running with a model loaded (for local backend)
echo 2. Or set TOGETHER_API_KEY environment variable (for cloud backend)
echo.
echo Press any key to start the application...
pause >nul

python main.py
>>>>>>> 0f3fe5ae72e1e543da9128827c74b2ea0a92d9d6
