FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (needed for compilation of some libs if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# PYTHONPATH setup if needed, but WORKDIR /app usually handles imports from .
ENV PYTHONPATH=/app
