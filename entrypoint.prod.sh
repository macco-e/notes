#!/bin/sh

# Waiting for mysql
echo "Waiting for mysql..."
sleep 10

# setup MySQL
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input --clear