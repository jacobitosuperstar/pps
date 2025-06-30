# Stage 1: Build environment with pipenv
FROM python:3-slim-bookworm AS builder

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT=1

# Set the working directory
WORKDIR /app/

# Install pipenv and dependencies
RUN python -m pip install --upgrade pip \
    && pip install pipenv

# Copy Pipfile.lock and install dependencies
COPY . .
RUN pipenv sync

# RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# USER appuser

# Exposing the port
EXPOSE 8000
