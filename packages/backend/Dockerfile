# Use Python 3.13 slim image
FROM python:3.13

# Set working directory
WORKDIR /app

# Install system dependencies and CA certificates
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

#RUN apt-get update && apt-get install -y curl-openssl ca-certificates

# Force OpenSSL/curl to use the correct CA bundle
#ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8090

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8090/health || exit 1

# Command to run the application
CMD ["python", "gateway_server.py"]
