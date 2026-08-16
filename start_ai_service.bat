@echo off
echo Starting SignLearn AI Service on port 8001...
echo.
cd /d "%~dp0AIML_CV"
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found. Install Python 3.9+ first.
    pause
    exit /b 1
)
pip install -r requirements.txt -q
echo.
echo Starting AI service at http://localhost:8001 ...
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001 --reload
pause
