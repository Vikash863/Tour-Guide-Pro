@echo off
chcp 65001 >nul
echo ============================================
echo   TourGuidePro - Fix & Run Website
echo ============================================
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Compiling translations...
.python.exe manage.py compilemessages

echo.
echo Starting server...
echo.
echo Your website will be available at: http://localhost:8000
echo.
.python.exe manage.py runserver

pause
