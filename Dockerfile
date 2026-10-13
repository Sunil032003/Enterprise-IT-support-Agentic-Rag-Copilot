# ==============================================================================
# Enterprise IT Support Agentic RAG Copilot - Multi-Stage / Production Dockerfile
# ==============================================================================
FROM python:3.11-slim AS base

# Set environment variables for Python runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app" \
    PORT=8000

# Install system dependencies (curl for healthcheck, build-essential for C extensions if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Create an unprivileged application user
RUN useradd -m -u 1000 appuser

# Copy dependency definition first for optimal layer caching
COPY requirements.txt /app/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ /app/app/
COPY data/ /app/data/
COPY static/ /app/static/
COPY templates/ /app/templates/
COPY run.py /app/run.py
COPY ingest_sample_kb.py /app/ingest_sample_kb.py

# Ensure uploads and data directories exist and set appropriate permissions
RUN mkdir -p /app/uploads /app/data && \
    chown -R appuser:appuser /app

# Switch to non-root user for security
USER appuser

# Expose FastAPI application port
EXPOSE 8000

# Container Healthcheck targeting FastAPI health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Launch the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

