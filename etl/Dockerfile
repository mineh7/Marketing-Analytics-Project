FROM python:3.10-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt 
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Environment variables for PostgreSQL connection
ENV DATABASE_URL=postgresql://admin:admin@db:5050/postgres

# Expose port 3000 (if needed for a web app)
EXPOSE 3000

# Command to run the script
CMD ["python", "create_tables.py"]
