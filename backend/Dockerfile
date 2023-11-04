# Base image with Python and pip preinstalled
# FROM python:3.11-slim-buster as base
FROM python:3.11-slim-bookworm as base

# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT=1

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN python -m pip install --upgrade pip \
    && pip install pipenv

# Copy only the Pipfile and install dependencies
COPY ./backend/Pipfile* /app/
RUN pipenv install --system --deploy

# Copy only necessary files and directories
COPY . /app/

# Exposing the port
EXPOSE 8000
