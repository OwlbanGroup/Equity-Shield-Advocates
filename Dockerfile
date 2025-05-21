# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHON_ENV production

# Create non-root user
RUN useradd -m -U appuser && \
    mkdir -p /app /var/log/equity-shield /var/run/equity-shield && \
    chown -R appuser:appuser /app /var/log/equity-shield /var/run/equity-shield

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY config/requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY --chown=appuser:appuser src /app/src
COPY --chown=appuser:appuser data /app/data
COPY --chown=appuser:appuser wsgi.py /app/
COPY --chown=appuser:appuser Procfile /app/

# Create directory for health checks
RUN mkdir -p /app/health && \
    chown -R appuser:appuser /app/health

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Volume configuration
VOLUME ["/var/log/equity-shield", "/var/run/equity-shield"]

# Run the application with waitress using the wsgi entry point
CMD ["python", "wsgi.py"]
