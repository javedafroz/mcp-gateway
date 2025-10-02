# Configuration module for MCP Gateway
import os
import json
import logging
from typing import Dict, List, Any, Optional, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

class LLMConfig(BaseSettings):
    """LLM Configuration Settings"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY", description="OpenAI API key")
    openai_model: str = Field("gpt-4o-mini", env="OPENAI_MODEL", description="OpenAI model name")
    openai_base_url: Optional[str] = Field(None, env="OPENAI_BASE_URL", description="Custom OpenAI base URL")
    openai_organization: Optional[str] = Field(None, env="OPENAI_ORGANIZATION", description="OpenAI organization ID")
    openai_api_version: Optional[str] = Field(None, env="OPENAI_API_VERSION", description="OpenAI API version")
    
    # Model Parameters
    temperature: float = Field(0.0, env="LLM_TEMPERATURE", description="Model temperature (0.0-2.0)")
    max_tokens: Optional[int] = Field(None, env="LLM_MAX_TOKENS", description="Maximum tokens to generate")
    top_p: float = Field(1.0, env="LLM_TOP_P", description="Top-p sampling parameter")
    frequency_penalty: float = Field(0.0, env="LLM_FREQUENCY_PENALTY", description="Frequency penalty (-2.0 to 2.0)")
    presence_penalty: float = Field(0.0, env="LLM_PRESENCE_PENALTY", description="Presence penalty (-2.0 to 2.0)")
    
    # Request Configuration
    request_timeout: float = Field(60.0, env="LLM_REQUEST_TIMEOUT", description="Request timeout in seconds")
    max_retries: int = Field(3, env="LLM_MAX_RETRIES", description="Maximum number of retries")
    retry_delay: float = Field(1.0, env="LLM_RETRY_DELAY", description="Delay between retries in seconds")
    
    # HTTP Client Configuration
    http_timeout: float = Field(30.0, env="HTTP_TIMEOUT", description="HTTP client timeout")
    http_verify_ssl: bool = Field(True, env="HTTP_VERIFY_SSL", description="Verify SSL certificates")
    http_max_connections: int = Field(100, env="HTTP_MAX_CONNECTIONS", description="Maximum HTTP connections")
    http_max_keepalive_connections: int = Field(20, env="HTTP_MAX_KEEPALIVE_CONNECTIONS", description="Maximum keepalive connections")
    
    # Streaming Configuration
    streaming: bool = Field(False, env="LLM_STREAMING", description="Enable streaming responses")
    stream_chunk_size: int = Field(1024, env="LLM_STREAM_CHUNK_SIZE", description="Streaming chunk size")
    
    # Model Fallback Configuration
    fallback_model: Optional[str] = Field(None, env="LLM_FALLBACK_MODEL", description="Fallback model if primary fails")
    enable_fallback: bool = Field(True, env="LLM_ENABLE_FALLBACK", description="Enable fallback to alternative initialization")
    
    @field_validator('temperature')
    @classmethod
    def validate_temperature(cls, v):
        if not 0.0 <= v <= 2.0:
            raise ValueError('Temperature must be between 0.0 and 2.0')
        return v
    
    @field_validator('top_p')
    @classmethod
    def validate_top_p(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Top-p must be between 0.0 and 1.0')
        return v
    
    @field_validator('frequency_penalty', 'presence_penalty')
    @classmethod
    def validate_penalties(cls, v):
        if not -2.0 <= v <= 2.0:
            raise ValueError('Penalties must be between -2.0 and 2.0')
        return v

class LangChainConfig(BaseSettings):
    """LangChain Configuration Settings"""
    
    # LangChain API Configuration
    langchain_api_key: Optional[str] = Field(None, env="LANGCHAIN_API_KEY", description="LangChain API key")
    langchain_endpoint: Optional[str] = Field(None, env="LANGCHAIN_ENDPOINT", description="LangChain endpoint URL")
    langchain_project: Optional[str] = Field(None, env="LANGCHAIN_PROJECT", description="LangChain project name")
    
    # Tracing and Monitoring
    langchain_tracing_v2: bool = Field(False, env="LANGCHAIN_TRACING_V2", description="Enable LangChain tracing v2")
    langsmith_api_key: Optional[str] = Field(None, env="LANGSMITH_API_KEY", description="LangSmith API key")
    langsmith_endpoint: Optional[str] = Field(None, env="LANGSMITH_ENDPOINT", description="LangSmith endpoint URL")
    
    # Agent Configuration
    agent_type: str = Field("react", env="AGENT_TYPE", description="Agent type (react, openai-functions, etc.)")
    agent_max_iterations: int = Field(15, env="AGENT_MAX_ITERATIONS", description="Maximum agent iterations")
    agent_max_execution_time: Optional[float] = Field(None, env="AGENT_MAX_EXECUTION_TIME", description="Maximum execution time in seconds")
    agent_early_stopping_method: str = Field("force", env="AGENT_EARLY_STOPPING_METHOD", description="Early stopping method")
    agent_verbose: bool = Field(False, env="AGENT_VERBOSE", description="Enable verbose agent logging")
    
    # Tool Configuration
    tool_timeout: float = Field(30.0, env="TOOL_TIMEOUT", description="Tool execution timeout")
    tool_max_retries: int = Field(2, env="TOOL_MAX_RETRIES", description="Maximum tool execution retries")
    tool_parallel_execution: bool = Field(True, env="TOOL_PARALLEL_EXECUTION", description="Enable parallel tool execution")
    
    # Memory Configuration
    memory_type: str = Field("buffer", env="MEMORY_TYPE", description="Memory type (buffer, summary, etc.)")
    memory_max_token_limit: int = Field(2000, env="MEMORY_MAX_TOKEN_LIMIT", description="Maximum tokens in memory")
    memory_return_messages: bool = Field(True, env="MEMORY_RETURN_MESSAGES", description="Return messages in memory")
    
    # Callback Configuration
    callbacks_enabled: bool = Field(True, env="CALLBACKS_ENABLED", description="Enable callbacks")
    callback_handlers: str = Field("", env="CALLBACK_HANDLERS", description="Comma-separated callback handler names")
    
    # Chain Configuration
    chain_type: str = Field("stuff", env="CHAIN_TYPE", description="Chain type for document processing")
    chain_verbose: bool = Field(False, env="CHAIN_VERBOSE", description="Enable verbose chain logging")

class MCPConfig(BaseSettings):
    """MCP (Model Context Protocol) Configuration Settings"""
    
    # MCP Server Configuration
    mcp_server_start_port: int = Field(9000, env="MCP_SERVER_START_PORT", description="Starting port for MCP servers")
    mcp_server_timeout: float = Field(30.0, env="MCP_SERVER_TIMEOUT", description="MCP server connection timeout")
    mcp_server_max_retries: int = Field(3, env="MCP_SERVER_MAX_RETRIES", description="Maximum MCP server connection retries")
    
    # Transport Configuration
    mcp_default_transport: str = Field("stdio", env="MCP_DEFAULT_TRANSPORT", description="Default MCP transport (stdio, streamable_http)")
    mcp_stdio_timeout: float = Field(30.0, env="MCP_STDIO_TIMEOUT", description="stdio transport timeout")
    mcp_http_timeout: float = Field(30.0, env="MCP_HTTP_TIMEOUT", description="HTTP transport timeout")
    
    # Tool Generation Configuration
    tool_generation_timeout: float = Field(60.0, env="TOOL_GENERATION_TIMEOUT", description="Tool generation timeout")
    tool_validation_enabled: bool = Field(True, env="TOOL_VALIDATION_ENABLED", description="Enable tool validation")
    tool_description_max_length: int = Field(500, env="TOOL_DESCRIPTION_MAX_LENGTH", description="Maximum tool description length")
    
    # Session Management
    session_timeout: float = Field(300.0, env="SESSION_TIMEOUT", description="Session timeout in seconds")
    session_cleanup_interval: float = Field(60.0, env="SESSION_CLEANUP_INTERVAL", description="Session cleanup interval")
    max_concurrent_sessions: int = Field(100, env="MAX_CONCURRENT_SESSIONS", description="Maximum concurrent sessions")

class GatewayConfig(BaseSettings):
    """Gateway Server Configuration Settings"""
    
    # Server Configuration
    host: str = Field("0.0.0.0", env="GATEWAY_HOST", description="Gateway host")
    port: int = Field(8090, env="GATEWAY_PORT", description="Gateway port")
    workers: int = Field(1, env="GATEWAY_WORKERS", description="Number of worker processes")
    
    # CORS Configuration
    cors_origins: str = Field(
        "http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080,http://127.0.0.1:8080",
        env="CORS_ORIGINS",
        description="Comma-separated CORS origins"
    )
    cors_credentials: bool = Field(True, env="CORS_CREDENTIALS", description="Allow CORS credentials")
    cors_methods: str = Field("GET,POST,PUT,DELETE,OPTIONS", env="CORS_METHODS", description="Allowed CORS methods")
    cors_headers: str = Field("*", env="CORS_HEADERS", description="Allowed CORS headers")
    
    # Rate Limiting
    rate_limit_enabled: bool = Field(False, env="RATE_LIMIT_ENABLED", description="Enable rate limiting")
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS", description="Requests per minute")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW", description="Rate limit window in seconds")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL", description="Logging level")
    log_format: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT", description="Log format")
    log_file: Optional[str] = Field(None, env="LOG_FILE", description="Log file path")
    
    # Security Configuration
    api_key_header: str = Field("X-API-Key", env="API_KEY_HEADER", description="API key header name")
    require_api_key: bool = Field(False, env="REQUIRE_API_KEY", description="Require API key for requests")
    allowed_api_keys: str = Field("", env="ALLOWED_API_KEYS", description="Comma-separated allowed API keys")
    
    @field_validator('cors_origins')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    @field_validator('cors_methods')
    @classmethod
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(',') if method.strip()]
        return v
    
    @field_validator('allowed_api_keys')
    @classmethod
    def parse_api_keys(cls, v):
        if isinstance(v, str):
            return [key.strip() for key in v.split(',') if key.strip()]
        return v

class CacheConfig(BaseSettings):
    """Cache Configuration Settings"""
    
    # Redis Configuration
    redis_enabled: bool = Field(False, env="REDIS_ENABLED", description="Enable Redis caching")
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL", description="Redis connection URL")
    redis_password: Optional[str] = Field(None, env="REDIS_PASSWORD", description="Redis password")
    redis_db: int = Field(0, env="REDIS_DB", description="Redis database number")
    redis_max_connections: int = Field(10, env="REDIS_MAX_CONNECTIONS", description="Maximum Redis connections")
    
    # Cache TTL Configuration
    cache_ttl_default: int = Field(300, env="CACHE_TTL_DEFAULT", description="Default cache TTL in seconds")
    cache_ttl_llm_responses: int = Field(3600, env="CACHE_TTL_LLM_RESPONSES", description="LLM response cache TTL")
    cache_ttl_tool_results: int = Field(1800, env="CACHE_TTL_TOOL_RESULTS", description="Tool result cache TTL")
    cache_ttl_sessions: int = Field(86400, env="CACHE_TTL_SESSIONS", description="Session cache TTL")
    
    # Memory Cache Configuration
    memory_cache_enabled: bool = Field(True, env="MEMORY_CACHE_ENABLED", description="Enable in-memory caching")
    memory_cache_max_size: int = Field(1000, env="MEMORY_CACHE_MAX_SIZE", description="Maximum memory cache entries")
    memory_cache_ttl: int = Field(300, env="MEMORY_CACHE_TTL", description="Memory cache TTL in seconds")

class Config:
    """Main configuration class that combines all configuration sections"""
    
    def __init__(self):
        self.llm = LLMConfig()
        self.langchain = LangChainConfig()
        self.mcp = MCPConfig()
        self.gateway = GatewayConfig()
        self.cache = CacheConfig()
        
        # Setup logging based on configuration
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.gateway.log_level.upper()),
            format=self.gateway.log_format,
            filename=self.gateway.log_file
        )
    
    def get_llm_kwargs(self) -> Dict[str, Any]:
        """Get LLM initialization kwargs"""
        kwargs = {
            'model': self.llm.openai_model,
            'openai_api_key': self.llm.openai_api_key,
            'temperature': self.llm.temperature,
            'request_timeout': self.llm.request_timeout,
            'max_retries': self.llm.max_retries,
            'top_p': self.llm.top_p,
            'frequency_penalty': self.llm.frequency_penalty,
            'presence_penalty': self.llm.presence_penalty,
        }
        
        # Add optional parameters if set
        if self.llm.max_tokens:
            kwargs['max_tokens'] = self.llm.max_tokens
        if self.llm.openai_base_url:
            kwargs['openai_api_base'] = self.llm.openai_base_url
        if self.llm.openai_organization:
            kwargs['openai_organization'] = self.llm.openai_organization
        if self.llm.openai_api_version:
            kwargs['openai_api_version'] = self.llm.openai_api_version
        
        return kwargs
    
    def get_http_client_kwargs(self) -> Dict[str, Any]:
        """Get HTTP client initialization kwargs"""
        import httpx
        
        return {
            'timeout': self.llm.http_timeout,
            'verify': self.llm.http_verify_ssl,
            'limits': httpx.Limits(
                max_connections=self.llm.http_max_connections,
                max_keepalive_connections=self.llm.http_max_keepalive_connections,
            )
        }
    
    def get_agent_kwargs(self) -> Dict[str, Any]:
        """Get agent initialization kwargs for create_react_agent"""
        kwargs = {}
        
        # Only add supported parameters for create_react_agent
        # Note: create_react_agent doesn't support max_iterations, max_execution_time, etc.
        # These would need to be handled at the graph execution level, not creation level
        
        if self.langchain.agent_verbose:
            kwargs['debug'] = self.langchain.agent_verbose
            
        return kwargs
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as list"""
        if isinstance(self.gateway.cors_origins, list):
            return self.gateway.cors_origins
        return [origin.strip() for origin in self.gateway.cors_origins.split(',') if origin.strip()]
    
    def get_cors_methods(self) -> List[str]:
        """Get CORS methods as list"""
        if isinstance(self.gateway.cors_methods, list):
            return self.gateway.cors_methods
        return [method.strip() for method in self.gateway.cors_methods.split(',') if method.strip()]
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return os.getenv('ENVIRONMENT', 'development').lower() == 'development'
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return os.getenv('ENVIRONMENT', 'development').lower() == 'production'

# Global configuration instance
config = Config()

# Export commonly used configurations
__all__ = [
    'Config',
    'LLMConfig', 
    'LangChainConfig',
    'MCPConfig',
    'GatewayConfig',
    'CacheConfig',
    'config'
]
