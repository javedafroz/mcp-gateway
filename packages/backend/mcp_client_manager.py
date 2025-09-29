# MCP Client Manager - Handles multiple MCP servers and chat processing
import asyncio
import logging
from typing import Dict, List, Tuple, Any, Optional

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
import os
import httpx
import ssl

logger = logging.getLogger(__name__)

class MCPClientManager:
    def __init__(self):
        self.servers: Dict[str, Dict[str, Any]] = {}
        self.client: Optional[MultiServerMCPClient] = None
        self.agent = None
        self.model = None
        
    async def initialize(self):
        """Initialize the MCP client manager"""
        try:
            # Create a custom async HTTP client with SSL verification disabled
            # NOTE: This is for development only - not recommended for production
            async_http_client = httpx.AsyncClient(
                verify=False,  # Disable SSL verification
                timeout=30.0
            )
            
            # Initialize ChatOpenAI with custom async HTTP client
            self.model = ChatOpenAI(
                model="gpt-4o-mini",
                openai_api_key=os.getenv("OPENAI_API_KEY"),
                http_async_client=async_http_client,
                temperature=0
            )
            
            logger.info("MCP Client Manager initialized with SSL verification disabled (async)")
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            # Fallback to default initialization
            try:
                self.model = init_chat_model("openai:gpt-4o-mini")
                logger.info("MCP Client Manager initialized with default configuration")
            except Exception as fallback_error:
                logger.error(f"Fallback initialization also failed: {fallback_error}")
                raise
    
    async def add_server(self, name: str, config: Dict[str, Any]):
        """Add a new MCP server configuration"""
        self.servers[name] = config
        await self._rebuild_client()
        logger.info(f"Added MCP server: {name}")
    
    async def add_direct_tools(self, name: str, tools: List[Any]):
        """Add tools directly without going through MCP server"""
        # For now, we'll create a simple agent with these tools directly
        if not hasattr(self, 'direct_tools'):
            self.direct_tools = {}
        
        self.direct_tools[name] = tools
        await self._rebuild_client_with_direct_tools()
        logger.info(f"Added {len(tools)} direct tools for: {name}")
    
    async def remove_direct_tools(self, name: str):
        """Remove direct tools for a service"""
        if hasattr(self, 'direct_tools') and name in self.direct_tools:
            tools_count = len(self.direct_tools[name])
            del self.direct_tools[name]
            await self._rebuild_client_with_direct_tools()
            logger.info(f"Removed {tools_count} direct tools for: {name}")
        else:
            logger.warning(f"No direct tools found for service: {name}")
    
    async def remove_server(self, name: str):
        """Remove an MCP server"""
        if name in self.servers:
            del self.servers[name]
            await self._rebuild_client()
            logger.info(f"Removed MCP server: {name}")
        
        if hasattr(self, 'direct_tools') and name in self.direct_tools:
            del self.direct_tools[name]
            await self._rebuild_client_with_direct_tools()
            logger.info(f"Removed direct tools for: {name}")
    
    async def _rebuild_client(self):
        """Rebuild the MCP client with current server configurations"""
        if not self.servers:
            self.client = None
            self.agent = None
            return
            
        try:
            # Create new client with all servers
            self.client = MultiServerMCPClient(self.servers)
            
            # Get tools from all servers
            tools = await self.client.get_tools()
            
            # Create new agent with tools
            self.agent = create_react_agent(self.model, tools)
            
            logger.info(f"Rebuilt MCP client with {len(self.servers)} servers and {len(tools)} tools")
            
        except Exception as e:
            logger.error(f"Failed to rebuild MCP client: {e}")
            self.client = None
            self.agent = None
            raise
    
    async def _rebuild_client_with_direct_tools(self):
        """Rebuild the agent with direct tools (bypass MCP servers)"""
        try:
            # Collect all direct tools
            all_tools = []
            if hasattr(self, 'direct_tools'):
                for service_name, tools in self.direct_tools.items():
                    all_tools.extend(tools)
            
            # Also add any MCP server tools if they exist
            if self.client:
                try:
                    mcp_tools = await self.client.get_tools()
                    all_tools.extend(mcp_tools)
                except Exception as e:
                    logger.warning(f"Could not get MCP tools: {e}")
            
            if all_tools:
                # Create new agent with all tools
                self.agent = create_react_agent(self.model, all_tools)
                logger.info(f"Rebuilt agent with {len(all_tools)} total tools")
            else:
                self.agent = None
                logger.info("No tools available, agent set to None")
                
        except Exception as e:
            logger.error(f"Failed to rebuild client with direct tools: {e}")
            raise
    
    async def process_message(self, message: str, session_id: str = "default") -> Tuple[str, List[str]]:
        """Process a chat message using available MCP tools"""
        if not self.agent:
            return "No MCP servers available. Please register a service first.", []
        
        try:
            # Process message with agent
            response = await self.agent.ainvoke({
                "messages": [{"role": "user", "content": message}]
            })
            
            # Extract response content and tools used
            response_content = ""
            tools_used = []
            
            if "messages" in response:
                messages = response["messages"]
                if messages:
                    last_message = messages[-1]
                    if hasattr(last_message, 'content'):
                        response_content = last_message.content
                    elif isinstance(last_message, dict) and 'content' in last_message:
                        response_content = last_message['content']
                
                # Extract tool calls from message history
                for msg in messages:
                    if hasattr(msg, 'tool_calls') and msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            tools_used.append(tool_call.get('name', 'unknown'))
                    elif isinstance(msg, dict) and 'tool_calls' in msg:
                        for tool_call in msg['tool_calls']:
                            tools_used.append(tool_call.get('name', 'unknown'))
            
            return response_content or str(response), list(set(tools_used))
            
        except Exception as e:
            logger.error(f"Message processing failed: {e}")
            return f"Error processing message: {str(e)}", []
    
    async def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        if not self.client:
            return []
        
        try:
            tools = await self.client.get_tools()
            return [tool.name for tool in tools]
        except Exception as e:
            logger.error(f"Failed to get tools: {e}")
            return []
    
    async def shutdown(self):
        """Cleanup resources"""
        if self.client:
            # Close client connections if needed
            pass
        logger.info("MCP Client Manager shutdown complete")
