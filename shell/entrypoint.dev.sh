#!/bin/sh

# Waiting for mysql
echo "Waiting for mysql..."
sleep 5

# setup MySQL
python manage.py makemigrations
python manage.py migrate