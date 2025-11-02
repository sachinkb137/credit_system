FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files including build.sh
COPY . .

# Change to the project directory
WORKDIR /app/credit_approval_system

# Collect static files (may fail without DB, that's ok)
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Use the build script from the parent directory
CMD ["bash", "/app/build.sh"]
