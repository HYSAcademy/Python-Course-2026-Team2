# Use official Python slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl build-essential git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Set work directory inside container
WORKDIR /app

# Copy Poetry files first for caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies without creating virtualenv (inside container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

# Copy only source code
COPY ./src /app/src

# Expose port FastAPI runs on
EXPOSE 8000

# Set working directory to where main.py is
WORKDIR /app/src/file_processing_api

# Run FastAPI with reload (dev)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]