#!/bin/bash

# Tour Guide Pro - Quick Start & Testing Script
# This script helps set up and test the application

set -e

echo "================================"
echo "Tour Guide Pro - Setup Script"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}Checking Python installation...${NC}"
python --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check .env file
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cat > .env << EOF
# Django Settings
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB
MONGODB_URI=mongodb://localhost:27017/tour

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
EOF
    echo -e "${GREEN}✓ .env file created. Please update with your settings.${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py makemigrations
python manage.py migrate
echo -e "${GREEN}✓ Migrations completed${NC}"

# Create superuser
echo -e "${YELLOW}Creating superuser...${NC}"
echo "Enter superuser credentials:"
python manage.py createsuperuser || echo -e "${YELLOW}Superuser creation skipped${NC}"

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

echo ""
echo -e "${GREEN}================================"
echo "✓ Setup Complete!"
echo "================================${NC}"
echo ""
echo "Next steps:"
echo "1. Run the server: python manage.py runserver"
echo "2. Visit: http://localhost:8000"
echo "3. Admin panel: http://localhost:8000/admin"
echo "4. API: http://localhost:8000/api"
echo ""
