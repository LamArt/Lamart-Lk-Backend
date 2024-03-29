#!/bin/bash
exec "$@"
cd lamart_lk

# collect static
echo "Collect static files"
python manage.py collectstatic

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000