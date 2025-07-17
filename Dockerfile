# Stage 1: Build the frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend source code
COPY frontend/ /app/frontend

# We don't have any build step for the frontend, so we just copy the files.

# Stage 2: Build the backend
FROM python:3.11-slim AS backend-builder

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY backend/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 3: Final image
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from backend-builder
COPY --from=backend-builder /app/wheels /wheels

# Install dependencies from wheels
RUN pip install --no-cache /wheels/*

# Copy backend source code
COPY backend/ /app/backend

# Copy gunicorn config
COPY gunicorn_conf.py /app/

# Copy frontend files
COPY --from=frontend-builder /app/frontend /app/frontend

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "main:app"]
