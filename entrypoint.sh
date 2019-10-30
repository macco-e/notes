#!/bin/sh

# Waiting for mysql
echo "Waiting for mysql..."
sleep 5

# setup MySQL
python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear