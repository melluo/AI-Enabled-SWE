# ---- Build Stage ----
FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python dependencies in a virtual environment
COPY requirements.txt .
RUN python -m venv /venv \
    && /venv/bin/pip install --upgrade pip \
    && /venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- Final Stage ----
FROM python:3.11-slim

ENV PATH="/venv/bin:$PATH"

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /venv /venv

# Copy application code
COPY app/main.py app/main.py

# Expose port
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/app"]