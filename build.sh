#!/bin/bash

# Change to the project directory
cd /app/credit_approval_system

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
python << END
import sys
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')
django.setup()

import time
from django.db import connection
from django.db.utils import OperationalError

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        connection.ensure_connection()
        print("Database connection successful!")
        break
    except OperationalError:
        attempt += 1
        if attempt >= max_attempts:
            print("Failed to connect to database after 30 attempts")
            sys.exit(1)
        print(f"Waiting for database... (attempt {attempt}/{max_attempts})")
        time.sleep(2)
END

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migrations may have failed but continuing..."

# Check if data needs to be ingested (only if no customers exist)
echo "Checking if data ingestion is needed..."
python << END
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval_system.settings')
django.setup()

from loans.models import Customer

# Check if any customers exist
if Customer.objects.count() == 0:
    print("No customers found. Running data ingestion...")
    os.system("python manage.py ingest_data")
    print("Data ingestion completed!")
else:
    print(f"Found {Customer.objects.count()} existing customers. Skipping data ingestion.")
END

# Start the server
echo "Starting Django server..."
PORT=${PORT:-8000}
python manage.py runserver 0.0.0.0:$PORT
