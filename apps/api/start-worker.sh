#!/bin/bash
# Celery Worker Entrypoint Script

# Allow Celery to run as root in containerized environments
export C_FORCE_ROOT=true

# Start Celery worker
celery -A app.worker worker --loglevel=info --concurrency=2
