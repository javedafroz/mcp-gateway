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
from config import config

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
        
        # 🔍 DEBUG: Log service registration details
        logger.info("🔧 SERVICE REGISTRATION STARTED")
        logger.info("="*70)
        logger.info(f"📝 Service Name: {config.name}")
        logger.info(f"🌐 Base URL: {config.base_url}")
        logger.info(f"📋 OpenAPI Version: {config.openapi_spec.get('openapi', 'unknown')}")
        logger.info(f"📊 API Title: {config.openapi_spec.get('info', {}).get('title', 'unknown')}")
        
        # Count paths and operations
        paths = config.openapi_spec.get('paths', {})
        total_operations = 0
        for path, methods in paths.items():
            for method in methods.keys():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                    total_operations += 1
        
        logger.info(f"🛤️  API Paths: {len(paths)}")
        logger.info(f"⚡ Total Operations: {total_operations}")
        
        try:
            logger.info("🔄 Generating MCP tools from OpenAPI specification...")
            
            # Generate MCP tools from OpenAPI spec
            server_port = await self.openapi_generator.create_mcp_server(
                name=config.name,
                openapi_spec=config.openapi_spec,
                base_url=config.base_url
            )
            
            # Get the generated tools and add them directly to the client manager
            server_info = self.openapi_generator.active_servers[config.name]
            tools = server_info["tools"]
            
            logger.info(f"✅ Generated {len(tools)} MCP tools")
            
            # Log each generated tool
            for i, tool in enumerate(tools, 1):
                tool_name = getattr(tool, 'name', 'unknown')
                tool_desc = getattr(tool, 'description', 'No description')[:100]
                logger.info(f"  🛠️  Tool {i}: {tool_name} - {tool_desc}")
            
            logger.info("🔄 Adding tools to MCP Client Manager...")
            await self.client_manager.add_direct_tools(config.name, tools)
            
            self.active_servers[config.name] = {
                "port": server_port,
                "config": config,
                "tools_count": len(tools)
            }
            
            logger.info("="*50)
            logger.info("✅ SERVICE REGISTRATION COMPLETED")
            logger.info("="*50)
            logger.info(f"🎯 Service: {config.name}")
            logger.info(f"🔧 Tools Generated: {len(tools)}")
            logger.info(f"🚀 Port Assigned: {server_port}")
            logger.info(f"📊 Total Active Services: {len(self.active_servers)}")
            logger.info("="*70)
            
            return f"Service {config.name} registered successfully with {len(tools)} tools"
            
        except Exception as e:
            logger.error("💥 SERVICE REGISTRATION FAILED")
            logger.error("="*50)
            logger.error(f"🔥 Failed to register OpenAPI service {config.name}")
            logger.error(f"📝 Error: {e}")
            logger.error(f"🔍 Error Type: {type(e).__name__}")
            import traceback
            logger.error(f"📚 Traceback:\n{traceback.format_exc()}")
            logger.error("="*70)
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
        
        # 🔍 DEBUG: Log incoming chat request at gateway level
        logger.info("🌟 GATEWAY CHAT REQUEST")
        logger.info("="*70)
        logger.info(f"📨 Received chat request from client")
        logger.info(f"💬 Message: {request.message}")
        logger.info(f"🔑 Session ID: {request.session_id}")
        logger.info(f"📊 Active Services: {len(self.active_servers)}")
        logger.info(f"🔧 Available Services: {list(self.active_servers.keys())}")
        
        try:
            # Get response from MCP client manager
            logger.info("🔄 Forwarding to MCP Client Manager...")
            
            response, tools_used = await self.client_manager.process_message(
                message=request.message,
                session_id=request.session_id
            )
            
            # 🔍 DEBUG: Log gateway response
            logger.info("📤 GATEWAY RESPONSE")
            logger.info("="*50)
            logger.info(f"🎯 Tools Used: {tools_used}")
            logger.info(f"📝 Response Length: {len(response)} characters")
            response_preview = response[:200] + "..." if len(response) > 200 else response
            logger.info(f"💭 Response Preview: {response_preview}")
            logger.info("="*70)
            
            return ChatResponse(
                response=response,
                tools_used=tools_used,
                session_id=request.session_id
            )
            
        except Exception as e:
            logger.error("💥 GATEWAY CHAT ERROR")
            logger.error("="*50)
            logger.error(f"🔥 Error in gateway chat processing: {e}")
            logger.error(f"📝 Error Type: {type(e).__name__}")
            import traceback
            logger.error(f"📚 Traceback:\n{traceback.format_exc()}")
            logger.error("="*70)
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

# Add CORS middleware with configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get_cors_origins(),
    allow_credentials=config.gateway.cors_credentials,
    allow_methods=config.get_cors_methods(),
    allow_headers=[config.gateway.cors_headers] if config.gateway.cors_headers != "*" else ["*"],
)

@app.post("/register-service", response_model=Dict[str, str])
async def register_service(service_config: OpenAPIConfig):
    """Register a new service from OpenAPI specification"""
    result = await gateway.register_openapi_service(service_config)
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
        host=config.gateway.host,
        port=config.gateway.port,
        workers=config.gateway.workers,
        reload=config.is_development(),
        log_level=config.gateway.log_level.lower(),
        access_log=config.is_development()
    )
