# MCP Gateway Docker Setup

This document provides comprehensive instructions for running the MCP Gateway using Docker and Docker Compose.

## 🚀 Quick Start

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- Your OpenAI API key

### 1. Setup Environment

```bash
# Copy environment template
cp docker.env.example .env

# Edit .env file and add your OpenAI API key
nano .env
```

### 2. Start Development Environment

```bash
# Using the convenience script
./docker-run.sh dev --build --detach

# Or using docker-compose directly
docker-compose -f docker-compose.dev.yml up --build -d
```

### 3. Test the Gateway

```bash
# Check health
curl http://localhost:8090/health

# View API documentation
open http://localhost:8090/docs

# Register a service and test
./docker-run.sh test
```

## 📋 Available Commands

The `docker-run.sh` script provides convenient commands:

```bash
# Development
./docker-run.sh dev           # Start development environment
./docker-run.sh dev --build   # Build and start development environment
./docker-run.sh dev --detach  # Start in background

# Production
./docker-run.sh prod --detach # Start production environment

# Management
./docker-run.sh build         # Build Docker images
./docker-run.sh stop          # Stop all services
./docker-run.sh clean         # Clean up all resources
./docker-run.sh logs          # View logs
./docker-run.sh logs --follow # Follow logs
./docker-run.sh health        # Check service health
./docker-run.sh shell         # Open shell in container

# Testing
./docker-run.sh test          # Run integration tests
```

## 🏗️ Docker Compose Configurations

### Development (`docker-compose.dev.yml`)

**Features:**
- Hot reloading with volume mounts
- Debug logging enabled
- Direct access to source code

**Services:**
- `mcp-gateway`: Main application with hot reload

**Ports:**
- Gateway: `8090`

### Production (`docker-compose.prod.yml`)

**Features:**
- Optimized for production deployment
- Nginx reverse proxy with rate limiting
- Redis for session storage
- Resource limits and health checks
- Optional monitoring stack

**Services:**
- `mcp-gateway`: Main application
- `nginx`: Reverse proxy with SSL termination
- `redis`: Session storage and caching
- `prometheus`: Metrics collection (optional)
- `grafana`: Monitoring dashboard (optional)

**Ports:**
- HTTP: `80`
- HTTPS: `443`
- Gateway (direct): `8090`
- Redis: `6379`
- Prometheus: `9090` (monitoring profile)
- Grafana: `3000` (monitoring profile)

### Basic (`docker-compose.yml`)

**Features:**
- Simple setup for testing
- Minimal resource usage
- Optional services via profiles

**Profiles:**
- `testing`: Includes mock API service
- `production`: Includes Redis and Nginx

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `GATEWAY_HOST` | Host to bind to | `0.0.0.0` | No |
| `GATEWAY_PORT` | Port to listen on | `8090` | No |
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `OPENAI_MODEL` | AI model to use | `gpt-4o-mini` | No |

### Volume Mounts

**Development:**
- `.:/app` - Source code for hot reloading
- `/app/venv` - Exclude virtual environment

**Production:**
- `mcp_data:/app/data` - Persistent application data
- `redis_data:/data` - Redis persistence
- `./nginx.conf:/etc/nginx/nginx.conf:ro` - Nginx configuration

## 🚦 Service Health Checks

All services include health checks:

```bash
# Check individual service health
docker-compose ps

# Check application health endpoint
curl http://localhost:8090/health

# Use convenience script
./docker-run.sh health
```

## 📊 Monitoring (Production)

Enable monitoring stack:

```bash
# Start with monitoring
docker-compose -f docker-compose.prod.yml --profile monitoring up -d

# Access monitoring
open http://localhost:9090  # Prometheus
open http://localhost:3000  # Grafana (admin/admin)
```

## 🔒 Security Features

### Nginx Security Headers
- X-Frame-Options
- X-XSS-Protection
- X-Content-Type-Options
- Content-Security-Policy

### Rate Limiting
- 10 requests/second per IP
- Burst allowance of 20 requests
- Bypass for health checks

### Network Isolation
- All services run in isolated Docker network
- Only necessary ports exposed

## 🐛 Debugging

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs mcp-gateway

# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100
```

### Access Container Shell
```bash
# Gateway container
./docker-run.sh shell

# Or directly
docker-compose exec mcp-gateway /bin/bash
```

### Debug Mode
```bash
# Start with debug logging
LOG_LEVEL=DEBUG docker-compose -f docker-compose.dev.yml up
```

## 📈 Performance Tuning

### Resource Limits (Production)
```yaml
deploy:
  resources:
    limits:
      cpus: '2.0'
      memory: 2G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Scaling
```bash
# Scale gateway service
docker-compose -f docker-compose.prod.yml up --scale mcp-gateway=3 -d
```

## 🔄 Updates and Deployment

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
./docker-run.sh prod --build --detach
```

### Zero-Downtime Deployment
```bash
# Build new image
docker-compose -f docker-compose.prod.yml build

# Rolling update
docker-compose -f docker-compose.prod.yml up -d --no-deps mcp-gateway
```

## 📝 Backup and Recovery

### Backup Data
```bash
# Backup volumes
docker run --rm -v mcp_data:/data -v $(pwd):/backup alpine tar czf /backup/mcp_data.tar.gz -C /data .
docker run --rm -v redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis_data.tar.gz -C /data .
```

### Restore Data
```bash
# Restore volumes
docker run --rm -v mcp_data:/data -v $(pwd):/backup alpine tar xzf /backup/mcp_data.tar.gz -C /data
docker run --rm -v redis_data:/data -v $(pwd):/backup alpine tar xzf /backup/redis_data.tar.gz -C /data
```

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port
lsof -i :8090

# Stop conflicting services
./docker-run.sh stop
```

**Permission Issues:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

**Out of Memory:**
```bash
# Check Docker resource usage
docker stats

# Clean up unused resources
docker system prune -a
```

**Service Won't Start:**
```bash
# Check logs
docker-compose logs mcp-gateway

# Verify environment
docker-compose config
```

### Reset Everything
```bash
# Nuclear option - removes everything
./docker-run.sh clean
docker system prune -a --volumes
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [MCP Gateway API Documentation](http://localhost:8090/docs)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)

## 🤝 Contributing

When contributing Docker-related changes:

1. Test with both development and production configurations
2. Update this documentation
3. Ensure security best practices
4. Test resource limits and scaling
5. Verify health checks work correctly
