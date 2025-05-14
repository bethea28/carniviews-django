# Use a slim Python image to reduce size
FROM python:3.9-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=carniviews_django.settings

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements file first (for Docker cache efficiency)
COPY requirements.txt /app/

# Replace psycopg2 with psycopg2-binary
RUN sed -i 's/^psycopg2[>=<].*/psycopg2-binary>=2.9.10/' requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Ensure manage.py is executable
RUN chmod +x manage.py

# Expose Django development server port
EXPOSE 8000

# Run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
