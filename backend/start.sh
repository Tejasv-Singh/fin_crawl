#!/bin/sh
set -e

# Ensure data directory exists
mkdir -p /var/lib/data/local_data

# Run Alembic migrations if we had them (Skipping for MVP)
# alembic upgrade head

# Start Uvicorn
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
