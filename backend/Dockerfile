FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application preserving the 'backend' package structure
# We need to create the directory structure so imports like 'backend.src...' work
RUN mkdir -p backend/src
COPY src/ ./backend/src/
COPY __init__.py ./backend/

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Set PYTHONPATH to include /app so 'backend' can be imported
ENV PYTHONPATH=/app

EXPOSE 7860

CMD ["uvicorn", "backend.src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]