# MCP Gateway

A production-ready middleware service that converts OpenAPI specifications into Model Context Protocol (MCP) servers, featuring a React frontend with Keycloak authentication and AI-powered chat interface.

![MCP Gateway Architecture](https://img.shields.io/badge/Architecture-Monorepo-blue) ![Frontend](https://img.shields.io/badge/Frontend-React%20TypeScript-61dafb) ![Backend](https://img.shields.io/badge/Backend-FastAPI%20Python-009688) ![Auth](https://img.shields.io/badge/Auth-Keycloak-red) ![AI](https://img.shields.io/badge/AI-OpenAI%20GPT--4-purple)

## 🌟 Features

### 🎨 Frontend (React + TypeScript)
- **🔐 Authentication**: Mock authentication system (Keycloak-ready)
- **📋 Service Management**: List, register, and delete OpenAPI services
- **📁 Multiple Input Methods**: Upload OpenAPI files or paste JSON directly
- **💬 AI Chat Interface**: Natural language interaction with registered APIs
- **📱 Responsive Design**: Modern UI with Tailwind CSS and Headless UI
- **🔄 Real-time Updates**: Live service status and chat responses
- **🛡️ Type Safety**: Comprehensive TypeScript implementation

### 🔧 Backend (FastAPI + Python)
- **🔌 Dynamic OpenAPI to MCP Conversion**: Automatic tool generation
- **🤖 LangChain Integration**: Powered by OpenAI GPT-4
- **🔒 CORS Configuration**: Secure cross-origin requests
- **📊 Health Monitoring**: Comprehensive logging and monitoring
- **🐳 Docker Ready**: Multi-stage builds and containerization
- **⚡ Async Performance**: High-performance async/await architecture

### 🏗️ Architecture
- **📦 Monorepo Structure**: Organized workspace with npm workspaces
- **🔄 Full Stack Integration**: Seamless frontend-backend communication
- **🗄️ Database Support**: PostgreSQL with Redis caching
- **🚀 Production Ready**: Docker Compose orchestration
- **📈 Scalable**: Microservices architecture

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm 8+
- **Python** 3.13+
- **Docker** and Docker Compose (recommended)
- **OpenAI API Key** (for chat functionality)

### 🏃‍♂️ One-Command Setup

```bash
git clone <your-repo>
cd mcp-gateway
./setup.sh
```

### 🛠️ Manual Setup

1. **Install root dependencies:**
   ```bash
   npm install
   ```

2. **Install frontend dependencies:**
   ```bash
   cd packages/frontend
   npm install
   cd ../..
   ```

3. **Install backend dependencies:**
   ```bash
   cd packages/backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd ../..
   ```

4. **Configure environment:**
   ```bash
   # Copy environment templates
   cp packages/frontend/env.example packages/frontend/.env
   
   # Create backend .env file
   cat > packages/backend/.env << EOF
   OPENAI_API_KEY=your_openai_api_key_here
   KEYCLOAK_SERVER_URL=http://localhost:1010
   KEYCLOAK_REALM=mcp-gateway
   KEYCLOAK_CLIENT_ID=mcp-gateway-backend
   GATEWAY_HOST=0.0.0.0
   GATEWAY_PORT=8090
   LOG_LEVEL=INFO
   EOF
   ```

5. **Start development servers:**
   ```bash
   npm run dev  # Runs both frontend and backend
   ```

## 🐳 Docker Deployment

### Development Environment

```bash
# Start all services (recommended)
docker-compose -f docker-compose.full.yml up --build --detach

# Or use the convenience script
./docker-run.sh dev
```

### Production Environment

```bash
# Production deployment with Nginx and monitoring
docker-compose -f docker-compose.prod.yml up --build --detach
```

## 🌐 Access Points

Once running, access these endpoints:

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Frontend** | http://localhost:3000 | React UI Dashboard |
| 🔧 **Backend API** | http://localhost:8090 | REST API & Documentation |
| 📚 **API Docs** | http://localhost:8090/docs | Interactive API Documentation |
| 🔐 **Keycloak** | http://localhost:1010 | Identity & Access Management |
| 📊 **Health Check** | http://localhost:8090/health | Service Health Status |

### Default Keycloak Credentials
- **Username:** `admin`
- **Password:** `admin_password`

## 📖 Usage Guide

### 1. 📋 Service Management

#### Register a New Service

**Via UI:**
1. Navigate to http://localhost:3000/services
2. Click "Register Service"
3. Fill in service details:
   - **Name:** Your service identifier
   - **Base URL:** API endpoint (e.g., `https://api.example.com`)
   - **OpenAPI Spec:** Upload file or paste JSON

**Via API:**
```bash
curl -X POST "http://localhost:8090/register-service" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "employee_service",
    "base_url": "https://api.company.com",
    "openapi_spec": {
      "openapi": "3.1.0",
      "info": {
        "title": "Employee API",
        "version": "1.0.0"
      },
      "paths": {
        "/employees": {
          "get": {
            "summary": "List employees",
            "operationId": "list_employees"
          }
        }
      }
    }
  }'
```

#### View Registered Services

**Via UI:** Visit http://localhost:3000/services

**Via API:**
```bash
curl http://localhost:8090/services
```

#### Delete a Service

**Via UI:** Click the delete button on any service card

**Via API:**
```bash
curl -X DELETE "http://localhost:8090/delete-service/employee_service"
```

### 2. 💬 AI Chat Interface

#### Using the Chat UI

1. Navigate to http://localhost:3000/chat
2. Type natural language queries:
   - "List all employees in engineering department"
   - "What services are available?"
   - "Show me user with ID 123"
   - "Create a new project called 'MCP Gateway'"

#### Chat API

```bash
curl -X POST "http://localhost:8090/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get all employees",
    "session_id": "user_session_123"
  }'
```

**Response:**
```json
{
  "response": "I found 25 employees in the system. Here are the first 10...",
  "tools_used": ["list_employees"],
  "session_id": "user_session_123"
}
```

### 3. 🔧 API Reference

#### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/register-service` | Register new OpenAPI service |
| `DELETE` | `/delete-service/{name}` | Remove registered service |
| `GET` | `/services` | List all registered services |
| `POST` | `/chat` | Send chat message to AI |
| `GET` | `/health` | Service health check |

#### Service Registration Schema

```json
{
  "name": "string (required)",
  "base_url": "string (required, valid URL)",
  "openapi_spec": {
    "openapi": "3.0.0 | 3.1.0",
    "info": {
      "title": "string",
      "version": "string"
    },
    "paths": {
      // OpenAPI paths definition
    }
  }
}
```

#### Chat Request Schema

```json
{
  "message": "string (required)",
  "session_id": "string (optional)"
}
```

## 📁 Project Structure

```
mcp-gateway/
├── packages/
│   ├── backend/                 # Python FastAPI Backend
│   │   ├── gateway_server.py    # Main FastAPI application
│   │   ├── mcp_client_manager.py # MCP client management
│   │   ├── openapi_mcp_generator.py # OpenAPI to MCP conversion
│   │   ├── requirements.txt     # Python dependencies
│   │   ├── Dockerfile          # Backend container
│   │   └── docker-compose*.yml # Container orchestration
│   └── frontend/               # React TypeScript Frontend
│       ├── src/
│       │   ├── components/     # Reusable UI components
│       │   │   ├── Layout.tsx  # Main layout with navigation
│       │   │   ├── ServiceCard.tsx # Service display component
│       │   │   ├── ServiceRegistrationForm.tsx # Service creation form
│       │   │   ├── ChatInterface.tsx # AI chat component
│       │   │   ├── Modal.tsx   # Modal dialog component
│       │   │   ├── LoadingSpinner.tsx # Loading indicator
│       │   │   └── FileUpload.tsx # File upload component
│       │   ├── pages/          # Main application pages
│       │   │   ├── Dashboard.tsx # Overview and statistics
│       │   │   ├── Services.tsx  # Service management
│       │   │   └── Chat.tsx     # Chat interface
│       │   ├── hooks/          # Custom React hooks
│       │   │   ├── useAuth.tsx  # Authentication management
│       │   │   ├── useServices.ts # Service data management
│       │   │   └── useChat.ts   # Chat functionality
│       │   ├── services/       # API and external services
│       │   │   ├── api.ts      # Backend API client
│       │   │   └── keycloak.ts # Authentication service
│       │   └── types/          # TypeScript definitions
│       │       └── index.ts    # Type definitions
│       ├── public/             # Static assets
│       ├── Dockerfile         # Frontend container
│       ├── nginx.conf         # Production web server config
│       └── package.json       # Frontend dependencies
├── docker-compose.full.yml    # Complete stack deployment
├── setup.sh                   # Automated setup script
├── package.json              # Root workspace configuration
└── README.md                 # This file
```

## 🔧 Development

### Available Scripts

```bash
# Root level commands
npm run dev          # Start both frontend and backend
npm run build        # Build both packages
npm run test         # Run all tests
npm run lint         # Lint frontend code

# Frontend specific (from packages/frontend/)
npm start           # Start React development server
npm run build       # Build for production
npm test           # Run React tests
npm run lint       # ESLint with auto-fix

# Backend specific (from packages/backend/)
python gateway_server.py  # Start FastAPI server
pytest                    # Run Python tests (if available)
```

### Environment Configuration

#### Frontend Environment Variables

Create `packages/frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8090
REACT_APP_KEYCLOAK_URL=http://localhost:1010
REACT_APP_KEYCLOAK_REALM=mcp-gateway
REACT_APP_KEYCLOAK_CLIENT_ID=mcp-gateway-frontend
GENERATE_SOURCEMAP=false
```

#### Backend Environment Variables

Create `packages/backend/.env`:
```env
OPENAI_API_KEY=your_openai_api_key_here
KEYCLOAK_SERVER_URL=http://localhost:1010
KEYCLOAK_REALM=mcp-gateway
KEYCLOAK_CLIENT_ID=mcp-gateway-backend
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8090
LOG_LEVEL=INFO
```

### 🐛 Debugging

#### Backend Logs
```bash
# Docker logs
docker logs mcp-gateway-mcp-gateway-backend-1 --follow

# Local development
cd packages/backend
source venv/bin/activate
python gateway_server.py
```

#### Frontend Development
```bash
cd packages/frontend
npm start
# Visit http://localhost:3000 with browser dev tools
```

#### Health Checks
```bash
# Backend health
curl http://localhost:8090/health

# Frontend health
curl http://localhost:3000/health

# Keycloak health
curl http://localhost:1010/health/ready
```

## 🚀 Deployment

### Production Checklist

- [ ] Set secure `OPENAI_API_KEY`
- [ ] Configure Keycloak realm and clients
- [ ] Set up SSL certificates
- [ ] Configure environment-specific URLs
- [ ] Set up monitoring and logging
- [ ] Configure backup strategies
- [ ] Set resource limits in Docker

### Docker Production

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy with monitoring
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Scaling

The architecture supports horizontal scaling:

- **Frontend**: Scale Nginx instances behind load balancer
- **Backend**: Multiple FastAPI instances with shared Redis/PostgreSQL
- **Database**: PostgreSQL clustering and Redis Cluster
- **Authentication**: Keycloak clustering

## 🔒 Security

### Authentication Flow

1. **Frontend** authenticates with Keycloak
2. **JWT tokens** passed to backend APIs
3. **Backend** validates tokens with Keycloak
4. **Role-based** access control (configurable)

### Security Features

- **CORS Protection**: Configured for specific origins
- **JWT Validation**: Token-based authentication
- **Input Validation**: Pydantic models for API validation
- **SQL Injection Protection**: ORM-based database queries
- **XSS Protection**: React's built-in XSS protection
- **HTTPS Ready**: SSL termination at Nginx level

## 🤝 Contributing

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Install** dependencies: `npm run install:all`
4. **Make** your changes
5. **Test** your changes: `npm test`
6. **Lint** your code: `npm run lint`
7. **Commit** your changes: `git commit -m 'Add amazing feature'`
8. **Push** to the branch: `git push origin feature/amazing-feature`
9. **Open** a Pull Request

### Code Style

- **Frontend**: ESLint + Prettier
- **Backend**: Black + isort
- **TypeScript**: Strict mode enabled
- **Testing**: Jest (frontend) + pytest (backend)

## 📚 Examples

### Example OpenAPI Specification

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Employee Management API",
    "description": "Comprehensive employee management system",
    "version": "1.0.0"
  },
  "paths": {
    "/employees": {
      "get": {
        "summary": "List all employees",
        "operationId": "list_employees",
        "parameters": [
          {
            "name": "department",
            "in": "query",
            "schema": { "type": "string" }
          }
        ],
        "responses": {
          "200": {
            "description": "List of employees",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": { "$ref": "#/components/schemas/Employee" }
                }
              }
            }
          }
        }
      },
      "post": {
        "summary": "Create new employee",
        "operationId": "create_employee",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": { "$ref": "#/components/schemas/EmployeeCreate" }
            }
          }
        },
        "responses": {
          "201": {
            "description": "Employee created",
            "content": {
              "application/json": {
                "schema": { "$ref": "#/components/schemas/Employee" }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Employee": {
        "type": "object",
        "properties": {
          "id": { "type": "integer" },
          "name": { "type": "string" },
          "email": { "type": "string", "format": "email" },
          "department": { "type": "string" },
          "position": { "type": "string" }
        }
      },
      "EmployeeCreate": {
        "type": "object",
        "required": ["name", "email", "department"],
        "properties": {
          "name": { "type": "string" },
          "email": { "type": "string", "format": "email" },
          "department": { "type": "string" },
          "position": { "type": "string" }
        }
      }
    }
  }
}
```

### Chat Examples

```bash
# Natural language queries the AI can handle:

"List all employees in the engineering department"
→ Uses list_employees with department filter

"Create a new employee named John Doe in marketing"
→ Uses create_employee with provided data

"What's the current status of project Alpha?"
→ Uses relevant project management endpoints

"Show me all services that are currently registered"
→ Uses internal services endpoint

"Delete the user service"
→ Uses delete_service endpoint
```

## 🐛 Troubleshooting

### Common Issues

#### CORS Errors
```bash
# Symptom: Frontend can't connect to backend
# Solution: Check CORS configuration in gateway_server.py
curl -H "Origin: http://localhost:3000" http://localhost:8090/health
```

#### Container Won't Start
```bash
# Check container logs
docker logs mcp-gateway-mcp-gateway-backend-1
docker logs mcp-gateway-mcp-gateway-frontend-1

# Rebuild containers
docker-compose -f docker-compose.full.yml up --build --force-recreate
```

#### OpenAI API Errors
```bash
# Check API key is set
echo $OPENAI_API_KEY

# Test API connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

#### Keycloak Connection Issues
```bash
# Check Keycloak is running
curl http://localhost:1010/health/ready

# Check realm configuration
# Visit http://localhost:1010/admin
```

### Performance Optimization

- **Frontend**: Enable gzip compression in Nginx
- **Backend**: Use async/await throughout
- **Database**: Index frequently queried fields
- **Caching**: Implement Redis caching for API responses
- **CDN**: Serve static assets from CDN in production

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain** for MCP integration
- **FastAPI** for the excellent Python web framework
- **React** and **TypeScript** for the frontend
- **Keycloak** for authentication
- **OpenAI** for GPT-4 integration
- **Docker** for containerization

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Open a GitHub issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **API Documentation**: Visit http://localhost:8090/docs when running

---

**Built with ❤️ for the developer community**
