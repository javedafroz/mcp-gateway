# MCP Gateway

A middleware gateway that exposes chat endpoints backed by MCP (Model Context Protocol) servers dynamically generated from OpenAPI specifications.

## Architecture

```
Client Applications → Gateway (FastAPI) → MCP Client → MCP Servers → Target APIs
                         ↓
                   Chat Endpoint
                         ↓  
               LangGraph ReAct Agent
                         ↓
                   Dynamic MCP Tools
```

## Features

- **Dynamic MCP Server Generation**: Automatically creates MCP servers from OpenAPI specifications
- **Chat Interface**: RESTful chat endpoint that uses AI agents to interact with your APIs
- **Multiple Transport Support**: Supports both stdio and streamable-http transports
- **Service Management**: Register, list, and manage multiple API services
- **Tool Integration**: Seamlessly converts API operations into LangChain tools

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file from the example:
```bash
cp env_example.txt .env
```

Then edit `.env` and set your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

For comprehensive configuration options, see [CONFIGURATION.md](CONFIGURATION.md).

### 3. Start the Gateway

```bash
python gateway_server.py
```

The gateway will start on `http://localhost:8090`

### 4. Register a Service

Use the example OpenAPI specification:

```bash
curl -X POST "http://localhost:8090/register-service" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "user_service",
    "openapi_spec": {...},
    "base_url": "https://jsonplaceholder.typicode.com"
  }'
```

Or use the provided example script:
```bash
python example_usage.py
```

### 5. Chat with Your API

```bash
curl -X POST "http://localhost:8090/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Get me information about user with ID 1",
    "session_id": "my_session"
  }'
```

### 6. Delete a Service

To remove a registered service:

```bash
curl -X DELETE "http://localhost:8090/delete-service/user_service" \
  -H "accept: application/json"
```

## API Endpoints

### `POST /register-service`
Register a new API service from an OpenAPI specification.

**Request Body:**
```json
{
  "name": "service_name",
  "openapi_spec": { /* OpenAPI 3.0 specification */ },
  "base_url": "https://api.example.com"
}
```

### `DELETE /delete-service/{service_name}`
Delete a registered service.

**Path Parameter:**
- `service_name`: Name of the service to delete

**Response:**
```json
{
  "message": "Service service_name deleted successfully"
}
```

### `POST /chat`
Send a message to the AI agent that can use registered API tools.

**Request Body:**
```json
{
  "message": "Your question or request",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "AI agent response",
  "tools_used": ["tool1", "tool2"],
  "session_id": "session_id"
}
```

### `GET /services`
List all registered services and their details.

### `GET /health`
Health check endpoint.

## Example Usage

### Register a Service
```python
import aiohttp
import json

# Load your OpenAPI spec
with open("api_spec.json", "r") as f:
    spec = json.load(f)

# Register with gateway
async with aiohttp.ClientSession() as session:
    async with session.post("http://localhost:8090/register-service", json={
        "name": "my_api",
        "openapi_spec": spec,
        "base_url": "https://my-api.com"
    }) as response:
        result = await response.json()
        print(result)
```

### Chat with the Service
```python
async with aiohttp.ClientSession() as session:
    async with session.post("http://localhost:8090/chat", json={
        "message": "Get all users from the API",
        "session_id": "user123"
    }) as response:
        result = await response.json()
        print(result["response"])
```

## Components

### Gateway Server (`gateway_server.py`)
Main FastAPI application that handles HTTP requests and coordinates between components.

### MCP Client Manager (`mcp_client_manager.py`)
Manages multiple MCP server connections and provides a unified interface for tool execution.

### OpenAPI MCP Generator (`openapi_mcp_generator.py`)
Dynamically creates MCP servers from OpenAPI specifications by generating tool functions.

## Testing

Run the test suite:
```bash
python test_gateway.py
```

This will test:
- Gateway health
- Service registration
- Chat functionality
- Tool execution

## Configuration

The gateway uses the following default settings:
- Gateway port: 8090
- Generated MCP server ports: Starting from 9000
- AI Model: OpenAI GPT-4o-mini (configurable)

## Extending the Gateway

### Adding Custom Tools
You can extend the gateway by adding custom MCP tools or modifying the OpenAPI parser to handle specific API patterns.

### Custom AI Models
Modify the `MCPClientManager` to use different AI models by changing the model initialization.

### Transport Protocols
The gateway supports multiple MCP transport protocols. You can extend it to support additional transports as needed.

## Troubleshooting

### Common Issues

1. **OpenAI API Key**: Make sure your OpenAI API key is set in the environment
2. **Port Conflicts**: Ensure ports 8090+ are available
3. **OpenAPI Spec**: Validate your OpenAPI specification format
4. **Dependencies**: Install all required packages from requirements.txt

### Logs
The gateway provides detailed logging. Check the console output for debugging information.

## License

MIT License - see LICENSE file for details.
