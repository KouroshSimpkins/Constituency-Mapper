FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and ensure that output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set Poetry environment variables
ENV POETRY_VERSION=1.8.4
ENV POETRY_VIRTUALENVS_CREATE=false

ENV PATH="/root/.local/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y curl git build-essential \
    && curl -sSL https://install.python-poetry.org | python - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for the app
WORKDIR /app

# Copy the dependencies file to the working directory
COPY pyproject.toml poetry.lock /app/

# Install the dependencies
RUN poetry install --no-dev # --no-dev is used to avoid installing development dependencies

# Copy the rest of the code
COPY . /app/

# Run the application
CMD ["poetry", "run", "python", "app.py"]
