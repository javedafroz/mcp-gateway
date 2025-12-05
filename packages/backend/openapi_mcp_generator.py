# OpenAPI to MCP Server Generator
import asyncio
import json
import logging
import aiohttp
from typing import Dict, List, Any, Optional, Callable
from urllib.parse import urljoin
import threading
import uvicorn
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, create_model
from langchain_core.tools import tool
import inspect

logger = logging.getLogger(__name__)

class OpenAPIMCPGenerator:
    def __init__(self):
        self.active_servers: Dict[str, Dict[str, Any]] = {}
        self.port_counter = 9000  # Start from port 9000 for generated servers
        
    async def create_mcp_server(self, name: str, openapi_spec: Dict[str, Any], base_url: str) -> int:
        """Create and start an MCP server from OpenAPI specification"""
        try:
            port = self.port_counter
            self.port_counter += 1
            
            # Parse OpenAPI spec and create tools
            tools = self._parse_openapi_spec(openapi_spec, base_url)
            
            # For now, let's skip the actual server creation and just return the tools
            # We'll integrate them directly into the main MCP client
            self.active_servers[name] = {
                "port": port,
                "tools": tools,
                "base_url": base_url,
                "openapi_spec": openapi_spec
            }
            
            logger.info(f"Created MCP tools for '{name}' (simulated port {port})")
            return port
            
        except Exception as e:
            logger.error(f"Failed to create MCP server for {name}: {e}")
            raise
    
    def _parse_openapi_spec(self, spec: Dict[str, Any], base_url: str) -> List[Callable]:
        """Parse OpenAPI specification and create MCP tools"""
        tools = []
        
        # Get paths from OpenAPI spec
        paths = spec.get("paths", {})
        components = spec.get("components", {})
        schemas = components.get("schemas", {})
        
        for path, path_info in paths.items():
            for method, operation in path_info.items():
                if method.lower() in ["get", "post", "put", "delete", "patch"]:
                    tool = self._create_tool_from_operation(
                        path, method.upper(), operation, base_url, schemas
                    )
                    if tool:
                        tools.append(tool)
        
        logger.info(f"Generated {len(tools)} tools from OpenAPI spec")
        return tools
    
    def _create_tool_from_operation(
        self, 
        path: str, 
        method: str, 
        operation: Dict[str, Any], 
        base_url: str,
        schemas: Dict[str, Any]
    ) -> Optional[Callable]:
        """Create a tool function from an OpenAPI operation"""
        try:
            operation_id = operation.get("operationId", f"{method.lower()}_{path.replace('/', '_').replace('{', '').replace('}', '')}")
            
            # Ensure operation_id is within OpenAI's 64 character limit for function names
            if len(operation_id) > 64:
                # Try to create a shorter name while keeping it meaningful
                # Keep the method and main resource, truncate the rest
                parts = operation_id.split('_')
                if len(parts) > 3:
                    # Keep first part (method) and last meaningful parts
                    short_name = f"{parts[0]}_{parts[1]}"
                    if len(short_name) < 50:  # Leave room for more parts
                        for part in parts[2:]:
                            if len(short_name + '_' + part) <= 60:  # Leave some buffer
                                short_name += '_' + part
                            else:
                                break
                    operation_id = short_name
                
                # Final fallback: truncate to 64 chars
                if len(operation_id) > 64:
                    operation_id = operation_id[:64]
                    
            summary = operation.get("summary", f"{method} {path}")
            description = operation.get("description", summary)
            
            # Parse parameters
            parameters = operation.get("parameters", [])
            request_body = operation.get("requestBody", {})
            
            # Create function signature and body
            func_code = self._generate_function_code(
                operation_id, description, path, method, base_url, 
                parameters, request_body, schemas
            )
            
            # Execute the function code to create the actual function
            namespace = {
                'aiohttp': aiohttp,
                'json': json,
                'urljoin': urljoin,
                'logger': logger
            }
            exec(func_code, namespace)
            
            # Get the function and create a LangChain tool
            func = namespace[operation_id]
            func.__name__ = operation_id
            func.__doc__ = description
            
            # Create a LangChain tool using the @tool decorator
            langchain_tool = tool(func)
            
            return langchain_tool
            
        except Exception as e:
            logger.error(f"Failed to create tool for {method} {path}: {e}")
            return None
    
    def _generate_function_code(
        self,
        func_name: str,
        description: str,
        path: str,
        method: str,
        base_url: str,
        parameters: List[Dict],
        request_body: Dict,
        schemas: Dict
    ) -> str:
        """Generate Python function code for the API operation"""
        
        # Build parameter list
        param_list = []
        param_assignments = []
        
        # Path parameters
        path_params = [p for p in parameters if p.get("in") == "path"]
        query_params = [p for p in parameters if p.get("in") == "query"]
        
        for param in path_params + query_params:
            param_name = param["name"]
            param_type = self._get_python_type(param.get("schema", {}))
            required = param.get("required", False)
            
            if required:
                param_list.append(f"{param_name}: {param_type}")
            else:
                param_list.append(f"{param_name}: {param_type} = None")
        
        # Request body parameters
        if request_body:
            content = request_body.get("content", {})
            if "application/json" in content:
                schema = content["application/json"].get("schema", {})
                if schema:
                    param_list.append("request_data: dict = None")
        
        # Build the function
        func_code = f'''
async def {func_name}({", ".join(param_list)}) -> str:
    """{description}"""
    import aiohttp
    import json
    from urllib.parse import urljoin
    
    # Build URL
    url = urljoin("{base_url}", "{path}")
    
    # Replace path parameters
'''
        
        # Add path parameter replacements
        for param in path_params:
            param_name = param["name"]
            func_code += f'    url = url.replace("{{{param_name}}}", str({param_name}))\n'
        
        # Add query parameters
        if query_params:
            func_code += '''    
    # Build query parameters
    params = {}
'''
            for param in query_params:
                param_name = param["name"]
                func_code += f'''    if {param_name} is not None:
        params["{param_name}"] = {param_name}
'''
        
        # Add HTTP request with comprehensive logging
        func_code += f'''
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # 🔍 DEBUG: Log API request details
        logger.info("🌐 API REQUEST STARTED")
        logger.info("="*60)
        logger.info("🎯 Tool: {func_name}")
        logger.info("🔗 Method: {method}")
        logger.info(f"📍 URL: {{url}}")
        
        # Log parameters
        if 'params' in locals() and params:
            logger.info(f"🔍 Query Params: {{params}}")
        else:
            logger.info("🔍 Query Params: None")
'''
        
        if method in ["POST", "PUT", "PATCH"] and request_body:
            func_code += f'''        
        # Log request body for POST/PUT/PATCH
        if request_data:
            logger.info(f"📦 Request Body: {{request_data}}")
        else:
            logger.info("📦 Request Body: None")
        
        async with aiohttp.ClientSession() as session:
            logger.info(f"🚀 Executing {method} request to {{url}}")
            
            async with session.{method.lower()}(
                url, 
                json=request_data,
                params=params if 'params' in locals() else None
            ) as response:
'''
        else:
            func_code += f'''        
        async with aiohttp.ClientSession() as session:
            logger.info(f"🚀 Executing {method} request to {{url}}")
            
            async with session.{method.lower()}(
                url,
                params=params if 'params' in locals() else None
            ) as response:
'''
        
        func_code += '''                
                # 🔍 DEBUG: Log response details
                logger.info("📨 API RESPONSE RECEIVED")
                logger.info(f"📊 Status Code: {response.status}")
                logger.info(f"📋 Headers: {dict(response.headers)}")
                
                result_text = await response.text()
                
                if response.status == 200:
                    logger.info(f"✅ Success Response Length: {len(result_text)} characters")
                    
                    # Log response preview (first 500 chars)
                    preview = result_text[:500] + "..." if len(result_text) > 500 else result_text
                    logger.info(f"📄 Response Preview: {preview}")
                    
                    logger.info("="*60)
                    logger.info("✅ API REQUEST COMPLETED SUCCESSFULLY")
                    logger.info("="*60)
                    
                    return result_text
                else:
                    logger.error(f"❌ Error Response: {result_text}")
                    logger.error("="*60)
                    logger.error("❌ API REQUEST FAILED")
                    logger.error("="*60)
                    
                    return f"Error: HTTP {response.status} - {result_text}"
                    
    except Exception as e:
        logger.error("💥 API REQUEST EXCEPTION")
        logger.error("="*60)
        logger.error(f"🔥 Exception Type: {type(e).__name__}")
        logger.error(f"📝 Exception Message: {str(e)}")
        logger.error(f"🔍 Full Exception: {repr(e)}")
        import traceback
        logger.error(f"📚 Traceback:\\n{traceback.format_exc()}")
        logger.error("="*60)
        
        return f"Request failed: {str(e)}"
'''
        
        return func_code
    
    def _get_python_type(self, schema: Dict[str, Any]) -> str:
        """Convert OpenAPI schema type to Python type annotation"""
        schema_type = schema.get("type", "string")
        
        type_mapping = {
            "string": "str",
            "integer": "int", 
            "number": "float",
            "boolean": "bool",
            "array": "list",
            "object": "dict"
        }
        
        return type_mapping.get(schema_type, "str")
    
    async def shutdown(self):
        """Shutdown all active servers"""
        for name, server_info in self.active_servers.items():
            logger.info(f"Shutting down server: {name}")
            # Note: FastMCP servers running in threads are harder to gracefully shutdown
            # In a production environment, you'd want better lifecycle management
        
        self.active_servers.clear()
        logger.info("OpenAPI MCP Generator shutdown complete")
