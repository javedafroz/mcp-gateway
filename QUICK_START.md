# 🚀 MCP Gateway - Quick Start Guide

Get up and running with MCP Gateway in minutes!

## ⚡ One-Command Setup

```bash
git clone <your-repo>
cd mcp-gateway
./setup.sh
```

## 🐳 Docker Quick Start

```bash
# Start full stack
npm run docker:full

# Access the application
open http://localhost:3000
```

## 💻 Development Mode

```bash
# Install dependencies
npm run install:all

# Start development servers
npm run dev
```

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| 🎨 **Frontend** | http://localhost:3000 | Main UI |
| 🔧 **Backend** | http://localhost:8090 | REST API |
| 📚 **API Docs** | http://localhost:8090/docs | Swagger UI |
| 🔐 **Keycloak** | http://localhost:1010 | Auth (admin/admin_password) |

## 📋 Essential Commands

```bash
# Development
npm run dev              # Start both frontend & backend
npm run build           # Build for production
npm run test            # Run all tests
npm run lint            # Check code quality

# Docker
npm run docker:full     # Start full stack
npm run docker:logs     # View container logs
npm run docker:down     # Stop all containers

# Utilities
npm run health          # Check service health
npm run clean           # Clean all build artifacts
```

## 🔧 Quick API Test

```bash
# Check health
curl http://localhost:8090/health

# Register a service
curl -X POST "http://localhost:8090/register-service" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_service",
    "base_url": "https://jsonplaceholder.typicode.com",
    "openapi_spec": {
      "openapi": "3.0.0",
      "info": {"title": "Test API", "version": "1.0.0"},
      "paths": {
        "/users": {
          "get": {
            "summary": "List users",
            "operationId": "list_users"
          }
        }
      }
    }
  }'

# Test chat
curl -X POST "http://localhost:8090/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "List all users",
    "session_id": "test_session"
  }'
```

## 🐛 Troubleshooting

### CORS Issues
```bash
# Check CORS headers
curl -H "Origin: http://localhost:3000" http://localhost:8090/health -v
```

### Container Issues
```bash
# View logs
docker compose -f docker-compose.full.yml logs -f

# Restart services
docker compose -f docker-compose.full.yml restart
```

### Permission Issues
```bash
# Make setup script executable
chmod +x setup.sh

# Fix Docker permissions (if needed)
sudo chown -R $USER:$USER .
```

## 🎯 What to Try First

1. **Visit the UI**: http://localhost:3000
2. **Register a Service**: Use the "Register Service" button
3. **Try the Chat**: Ask "What services are available?"
4. **Check API Docs**: http://localhost:8090/docs

## 🔑 Environment Variables

Minimum required:
```bash
# Backend (.env)
OPENAI_API_KEY=your_api_key_here

# Frontend (.env)
REACT_APP_API_URL=http://localhost:8090
```

## 📞 Need Help?

- 📖 **Full Documentation**: See [README.md](./README.md)
- 🐛 **Issues**: Check existing issues or create new ones
- 💬 **Questions**: Use GitHub Discussions
- 🔧 **API Reference**: http://localhost:8090/docs

---

**Happy coding! 🎉**
