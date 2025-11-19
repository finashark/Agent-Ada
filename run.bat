@echo off
echo ========================================
echo   Agent Ada - Market Report System
echo   Starting application...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if requirements are installed
echo Checking dependencies...
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the application
echo Starting Streamlit application...
echo.
echo Application will open in your browser at:
echo http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo ========================================
echo.

streamlit run Home.py

pause
