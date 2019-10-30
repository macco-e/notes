#!/bin/sh

# Waiting for mysql
echo "Waiting for mysql..."
sleep 5

# setup db
python manage.py migrate