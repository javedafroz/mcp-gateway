# MCP Gateway Server - Main FastAPI application
import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from mcp_client_manager import MCPClientManager
from openapi_mcp_generator import OpenAPIMCPGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    tools_used: List[str] = []
    session_id: str

class OpenAPIConfig(BaseModel):
    name: str
    openapi_spec: Dict[str, Any]
    base_url: str

class GatewayServer:
    def __init__(self):
        self.client_manager = MCPClientManager()
        self.openapi_generator = OpenAPIMCPGenerator()
        self.active_servers: Dict[str, Any] = {}
        
    async def initialize(self):
        """Initialize the gateway server"""
        await self.client_manager.initialize()
        logger.info("MCP Gateway Server initialized")
        
    async def register_openapi_service(self, config: OpenAPIConfig) -> str:
        """Register a new service from OpenAPI specification"""
        try:
            # Generate MCP tools from OpenAPI spec
            server_port = await self.openapi_generator.create_mcp_server(
                name=config.name,
                openapi_spec=config.openapi_spec,
                base_url=config.base_url
            )
            
            # Get the generated tools and add them directly to the client manager
            server_info = self.openapi_generator.active_servers[config.name]
            tools = server_info["tools"]
            
            await self.client_manager.add_direct_tools(config.name, tools)
            
            self.active_servers[config.name] = {
                "port": server_port,
                "config": config,
                "tools_count": len(tools)
            }
            
            logger.info(f"Registered OpenAPI service: {config.name} with {len(tools)} tools")
            return f"Service {config.name} registered successfully with {len(tools)} tools"
            
        except Exception as e:
            logger.error(f"Failed to register OpenAPI service {config.name}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def delete_openapi_service(self, service_name: str) -> str:
        """Delete a registered OpenAPI service"""
        try:
            # Check if service exists
            if service_name not in self.active_servers:
                raise HTTPException(status_code=404, detail=f"Service {service_name} not found")
            
            # Remove from active servers
            service_info = self.active_servers.pop(service_name)
            
            # Remove from OpenAPI generator
            if service_name in self.openapi_generator.active_servers:
                del self.openapi_generator.active_servers[service_name]
            
            # Remove from client manager
            await self.client_manager.remove_direct_tools(service_name)
            
            logger.info(f"Deleted OpenAPI service: {service_name}")
            return f"Service {service_name} deleted successfully"
            
        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            logger.error(f"Failed to delete OpenAPI service {service_name}: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process chat request using available MCP tools"""
        try:
            # Get response from MCP client manager
            response, tools_used = await self.client_manager.process_message(
                message=request.message,
                session_id=request.session_id
            )
            
            return ChatResponse(
                response=response,
                tools_used=tools_used,
                session_id=request.session_id
            )
            
        except Exception as e:
            logger.error(f"Chat processing failed: {e}")
            raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
    
    async def shutdown(self):
        """Cleanup resources"""
        await self.client_manager.shutdown()
        await self.openapi_generator.shutdown()

# Global gateway instance
gateway = GatewayServer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await gateway.initialize()
    yield
    # Shutdown
    await gateway.shutdown()

# Create FastAPI app
app = FastAPI(
    title="MCP Gateway",
    description="A gateway server that exposes chat endpoints backed by MCP servers generated from OpenAPI specs",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React development server
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:8080",  # Alternative frontend port
        "http://127.0.0.1:8080",  # Alternative frontend port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.post("/register-service", response_model=Dict[str, str])
async def register_service(config: OpenAPIConfig):
    """Register a new service from OpenAPI specification"""
    result = await gateway.register_openapi_service(config)
    return {"message": result}

@app.delete("/delete-service/{service_name}", response_model=Dict[str, str])
async def delete_service(service_name: str):
    """Delete a registered service"""
    result = await gateway.delete_openapi_service(service_name)
    return {"message": result}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat endpoint that uses MCP tools to process requests"""
    return await gateway.chat(request)

@app.get("/services", response_model=Dict[str, Any])
async def list_services():
    """List all registered services"""
    return {
        "active_servers": list(gateway.active_servers.keys()),
        "details": gateway.active_servers
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "services": len(gateway.active_servers)}

if __name__ == "__main__":
    uvicorn.run(
        "gateway_server:app",
        host="0.0.0.0",
        port=8090,
        reload=True,
        log_level="info"
    )
