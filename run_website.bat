@echo off
chcp 65001 >nul
echo ============================================
echo   TourGuidePro - Fix & Run Website
echo ============================================
echo.
echo Compiling translations...
.venv\python.exe manage.py compilemessages

echo.
echo Starting server...
echo.
echo Your website will be available at: http://localhost:8000
echo.
.venv\python.exe manage.py runserver

pause
