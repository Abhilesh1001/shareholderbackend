#!/bin/bash
set -e

echo "Deployment started ..."

# Pull the latest version of the app
git pull origin main
echo "New changes copied to server !"

# Activate Virtual Env
source abhi/bin/activate
echo "Virtual env 'abhi' Activated !"

echo "Installing Dependencies..."
pip install -r requirements.txt --no-input

echo "Serving Static Files..."
python3 manage.py collectstatic --noinput

echo "Running Database migration"
python3 manage.py makemigrations
python3 manage.py migrate

# Deactivate Virtual Env
deactivate
echo "Virtual env 'abhi' Deactivated !"

# Reloading Application So New Changes could reflect on website
pushd shareholderloan
touch wsgi.py
popd

echo "Deployment Finished!"
