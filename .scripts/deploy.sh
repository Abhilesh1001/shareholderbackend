#!/bin/bash
set -e

echo "Deployment started ..."

# Navigate to the project directory
cd /var/www/shareholderbackend

# Pull the latest version of the app
echo "Pulling latest changes from Git..."
git pull origin master
echo "New changes copied to server!"

# Activate Virtual Env
echo "Activating virtual environment 'abhi'..."
source abhi/bin/activate
echo "Virtual environment 'abhi' activated!"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --no-input
echo "Dependencies installed!"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "Static files collected!"

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "Database migrations completed!"

# Deactivate Virtual Env
deactivate
echo "Virtual environment 'abhi' deactivated!"

# Reloading application to reflect new changes
echo "Reloading application..."
touch shareholderloan/wsgi.py
echo "Application reloaded!"

echo "Deployment finished!"