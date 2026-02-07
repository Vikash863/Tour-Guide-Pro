@echo off
REM Tour Guide Pro - Quick Start & Testing Script (Windows)

echo.
echo ================================
echo Tour Guide Pro - Setup Script
echo ================================
echo.

REM Check Python
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python not found. Please install Python first.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies
    exit /b 1
)
echo [OK] Dependencies installed

REM Check .env file
if not exist ".env" (
    echo Creating .env file...
    (
        echo # Django Settings
        echo SECRET_KEY=django-insecure-dev-key-change-in-production
        echo DEBUG=True
        echo ALLOWED_HOSTS=localhost,127.0.0.1
        echo.
        echo # MongoDB
        echo MONGODB_URI=mongodb://localhost:27017/tour
        echo.
        echo # CORS
        echo CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
    ) > .env
    echo [OK] .env file created. Please update with your settings.
) else (
    echo [OK] .env file already exists
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo [OK] Migrations completed

REM Create superuser
echo Creating superuser...
echo Enter superuser credentials:
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
echo [OK] Static files collected

echo.
echo ================================
echo [OK] Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Run the server: python manage.py runserver
echo 2. Visit: http://localhost:8000
echo 3. Admin panel: http://localhost:8000/admin
echo 4. API: http://localhost:8000/api
echo.
pause
