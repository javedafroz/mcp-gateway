# MCP Gateway Configuration Guide

## Overview

The MCP Gateway uses a comprehensive configuration system that allows you to customize all aspects of the LLM, LangChain, MCP, and gateway server behavior through environment variables. This guide explains all available configuration options.

## Configuration Structure

The configuration is organized into several sections:

- **LLM Configuration**: OpenAI model settings and parameters
- **LangChain Configuration**: Agent, tool, and chain settings
- **MCP Configuration**: Model Context Protocol server settings
- **Gateway Configuration**: FastAPI server and CORS settings
- **Cache Configuration**: Redis and memory caching settings

## Quick Start

1. Copy the example environment file:
   ```bash
   cp env_example.txt .env
   ```

2. Set your OpenAI API key:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Customize other settings as needed (all have sensible defaults)

## Configuration Sections

### 🤖 LLM Configuration

Controls the behavior of the Large Language Model (OpenAI GPT).

#### Required Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API key | - | `sk-...` |

#### Model Settings

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `OPENAI_MODEL` | OpenAI model name | `gpt-4o-mini` | `gpt-4`, `gpt-3.5-turbo` |
| `OPENAI_BASE_URL` | Custom OpenAI base URL | `https://api.openai.com/v1` | `https://api.openai.com/v1` |
| `OPENAI_ORGANIZATION` | OpenAI organization ID | - | `org-...` |
| `OPENAI_API_VERSION` | OpenAI API version | - | `2023-12-01-preview` |

#### Model Parameters

| Variable | Description | Default | Range | Example |
|----------|-------------|---------|-------|---------|
| `LLM_TEMPERATURE` | Model creativity/randomness | `0.0` | `0.0-2.0` | `0.7` |
| `LLM_MAX_TOKENS` | Maximum tokens to generate | - | `1-4096` | `2000` |
| `LLM_TOP_P` | Top-p sampling parameter | `1.0` | `0.0-1.0` | `0.9` |
| `LLM_FREQUENCY_PENALTY` | Frequency penalty | `0.0` | `-2.0-2.0` | `0.5` |
| `LLM_PRESENCE_PENALTY` | Presence penalty | `0.0` | `-2.0-2.0` | `0.5` |

#### Request Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LLM_REQUEST_TIMEOUT` | Request timeout (seconds) | `60.0` | `120.0` |
| `LLM_MAX_RETRIES` | Maximum retries | `3` | `5` |
| `LLM_RETRY_DELAY` | Delay between retries (seconds) | `1.0` | `2.0` |

#### HTTP Client Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `HTTP_TIMEOUT` | HTTP client timeout | `30.0` | `60.0` |
| `HTTP_VERIFY_SSL` | Verify SSL certificates | `true` | `false` |
| `HTTP_MAX_CONNECTIONS` | Maximum HTTP connections | `100` | `200` |
| `HTTP_MAX_KEEPALIVE_CONNECTIONS` | Maximum keepalive connections | `20` | `50` |

#### Streaming Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LLM_STREAMING` | Enable streaming responses | `false` | `true` |
| `LLM_STREAM_CHUNK_SIZE` | Streaming chunk size | `1024` | `2048` |

#### Fallback Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LLM_FALLBACK_MODEL` | Fallback model if primary fails | - | `gpt-3.5-turbo` |
| `LLM_ENABLE_FALLBACK` | Enable fallback initialization | `true` | `false` |

### 🔗 LangChain Configuration

Controls LangChain agent behavior and tool execution.

#### API Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LANGCHAIN_API_KEY` | LangChain API key | - | `lc_...` |
| `LANGCHAIN_ENDPOINT` | LangChain endpoint URL | - | `https://api.langchain.com` |
| `LANGCHAIN_PROJECT` | LangChain project name | - | `mcp-gateway` |

#### Tracing and Monitoring

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LANGCHAIN_TRACING_V2` | Enable LangChain tracing v2 | `false` | `true` |
| `LANGSMITH_API_KEY` | LangSmith API key | - | `ls_...` |
| `LANGSMITH_ENDPOINT` | LangSmith endpoint URL | - | `https://api.smith.langchain.com` |

#### Agent Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `AGENT_TYPE` | Agent type | `react` | `openai-functions` |
| `AGENT_MAX_ITERATIONS` | Maximum agent iterations | `15` | `20` |
| `AGENT_MAX_EXECUTION_TIME` | Maximum execution time (seconds) | - | `300.0` |
| `AGENT_EARLY_STOPPING_METHOD` | Early stopping method | `force` | `generate` |
| `AGENT_VERBOSE` | Enable verbose agent logging | `false` | `true` |

#### Tool Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TOOL_TIMEOUT` | Tool execution timeout | `30.0` | `60.0` |
| `TOOL_MAX_RETRIES` | Maximum tool execution retries | `2` | `3` |
| `TOOL_PARALLEL_EXECUTION` | Enable parallel tool execution | `true` | `false` |

#### Memory Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MEMORY_TYPE` | Memory type | `buffer` | `summary` |
| `MEMORY_MAX_TOKEN_LIMIT` | Maximum tokens in memory | `2000` | `4000` |
| `MEMORY_RETURN_MESSAGES` | Return messages in memory | `true` | `false` |

#### Callback Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `CALLBACKS_ENABLED` | Enable callbacks | `true` | `false` |
| `CALLBACK_HANDLERS` | Callback handler names | - | `console,file,langsmith` |

#### Chain Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `CHAIN_TYPE` | Chain type for document processing | `stuff` | `map_reduce` |
| `CHAIN_VERBOSE` | Enable verbose chain logging | `false` | `true` |

### 🔌 MCP Configuration

Controls Model Context Protocol server behavior.

#### Server Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MCP_SERVER_START_PORT` | Starting port for MCP servers | `9000` | `10000` |
| `MCP_SERVER_TIMEOUT` | MCP server connection timeout | `30.0` | `60.0` |
| `MCP_SERVER_MAX_RETRIES` | Maximum connection retries | `3` | `5` |

#### Transport Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MCP_DEFAULT_TRANSPORT` | Default MCP transport | `stdio` | `streamable_http` |
| `MCP_STDIO_TIMEOUT` | stdio transport timeout | `30.0` | `60.0` |
| `MCP_HTTP_TIMEOUT` | HTTP transport timeout | `30.0` | `60.0` |

#### Tool Generation Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `TOOL_GENERATION_TIMEOUT` | Tool generation timeout | `60.0` | `120.0` |
| `TOOL_VALIDATION_ENABLED` | Enable tool validation | `true` | `false` |
| `TOOL_DESCRIPTION_MAX_LENGTH` | Maximum tool description length | `500` | `1000` |

#### Session Management

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `SESSION_TIMEOUT` | Session timeout (seconds) | `300.0` | `600.0` |
| `SESSION_CLEANUP_INTERVAL` | Session cleanup interval | `60.0` | `120.0` |
| `MAX_CONCURRENT_SESSIONS` | Maximum concurrent sessions | `100` | `200` |

### 🌐 Gateway Configuration

Controls the FastAPI server and HTTP behavior.

#### Server Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `GATEWAY_HOST` | Gateway host | `0.0.0.0` | `127.0.0.1` |
| `GATEWAY_PORT` | Gateway port | `8090` | `8080` |
| `GATEWAY_WORKERS` | Number of worker processes | `1` | `4` |

#### CORS Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:3000,...` | `https://myapp.com` |
| `CORS_CREDENTIALS` | Allow CORS credentials | `true` | `false` |
| `CORS_METHODS` | Allowed CORS methods | `GET,POST,PUT,DELETE,OPTIONS` | `GET,POST` |
| `CORS_HEADERS` | Allowed CORS headers | `*` | `Content-Type,Authorization` |

#### Rate Limiting

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `RATE_LIMIT_ENABLED` | Enable rate limiting | `false` | `true` |
| `RATE_LIMIT_REQUESTS` | Requests per minute | `100` | `60` |
| `RATE_LIMIT_WINDOW` | Rate limit window (seconds) | `60` | `300` |

#### Logging Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `LOG_LEVEL` | Logging level | `INFO` | `DEBUG` |
| `LOG_FORMAT` | Log format | `%(asctime)s - %(name)s...` | Custom format |
| `LOG_FILE` | Log file path | - | `/var/log/mcp-gateway.log` |

#### Security Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `API_KEY_HEADER` | API key header name | `X-API-Key` | `Authorization` |
| `REQUIRE_API_KEY` | Require API key for requests | `false` | `true` |
| `ALLOWED_API_KEYS` | Allowed API keys | - | `key1,key2,key3` |

### 💾 Cache Configuration

Controls caching behavior for performance optimization.

#### Redis Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `REDIS_ENABLED` | Enable Redis caching | `false` | `true` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` | `redis://redis:6379` |
| `REDIS_PASSWORD` | Redis password | - | `password123` |
| `REDIS_DB` | Redis database number | `0` | `1` |
| `REDIS_MAX_CONNECTIONS` | Maximum Redis connections | `10` | `20` |

#### Cache TTL Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `CACHE_TTL_DEFAULT` | Default cache TTL (seconds) | `300` | `600` |
| `CACHE_TTL_LLM_RESPONSES` | LLM response cache TTL | `3600` | `7200` |
| `CACHE_TTL_TOOL_RESULTS` | Tool result cache TTL | `1800` | `3600` |
| `CACHE_TTL_SESSIONS` | Session cache TTL | `86400` | `172800` |

#### Memory Cache Configuration

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MEMORY_CACHE_ENABLED` | Enable in-memory caching | `true` | `false` |
| `MEMORY_CACHE_MAX_SIZE` | Maximum memory cache entries | `1000` | `2000` |
| `MEMORY_CACHE_TTL` | Memory cache TTL (seconds) | `300` | `600` |

## Environment-Specific Configuration

### Development Environment

```bash
ENVIRONMENT=development
LOG_LEVEL=DEBUG
HTTP_VERIFY_SSL=false
AGENT_VERBOSE=true
CHAIN_VERBOSE=true
```

### Production Environment

```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
HTTP_VERIFY_SSL=true
GATEWAY_WORKERS=4
REDIS_ENABLED=true
RATE_LIMIT_ENABLED=true
```

## Configuration Validation

The configuration system includes validation for:

- **Range validation**: Temperature (0.0-2.0), penalties (-2.0-2.0)
- **Type validation**: Booleans, integers, floats
- **Format validation**: URLs, comma-separated lists
- **Required field validation**: OpenAI API key

## Usage Examples

### High-Performance Configuration

```bash
# Optimized for high throughput
GATEWAY_WORKERS=4
HTTP_MAX_CONNECTIONS=200
HTTP_MAX_KEEPALIVE_CONNECTIONS=50
REDIS_ENABLED=true
MEMORY_CACHE_ENABLED=true
TOOL_PARALLEL_EXECUTION=true
```

### Creative AI Configuration

```bash
# More creative responses
LLM_TEMPERATURE=0.8
LLM_TOP_P=0.9
LLM_FREQUENCY_PENALTY=0.2
LLM_PRESENCE_PENALTY=0.2
```

### Debug Configuration

```bash
# Enhanced debugging
LOG_LEVEL=DEBUG
AGENT_VERBOSE=true
CHAIN_VERBOSE=true
LANGCHAIN_TRACING_V2=true
```

### Secure Production Configuration

```bash
# Production security
REQUIRE_API_KEY=true
ALLOWED_API_KEYS=prod_key_1,prod_key_2
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=60
HTTP_VERIFY_SSL=true
```

## Configuration Loading

The configuration is loaded in this order:

1. **Default values** from the configuration classes
2. **Environment variables** from the system
3. **`.env` file** in the backend directory
4. **`.env.local`** file for local overrides (if exists)

## Troubleshooting

### Common Issues

1. **Invalid temperature value**
   ```
   Error: Temperature must be between 0.0 and 2.0
   ```
   Solution: Set `LLM_TEMPERATURE` to a value between 0.0 and 2.0

2. **Missing OpenAI API key**
   ```
   Error: OPENAI_API_KEY is required
   ```
   Solution: Set `OPENAI_API_KEY` in your `.env` file

3. **CORS issues**
   ```
   Error: CORS policy blocked request
   ```
   Solution: Add your frontend URL to `CORS_ORIGINS`

4. **Connection timeout**
   ```
   Error: Request timeout
   ```
   Solution: Increase `LLM_REQUEST_TIMEOUT` or `HTTP_TIMEOUT`

### Validation Errors

The configuration system will show detailed validation errors on startup:

```bash
ValidationError: 2 validation errors for LLMConfig
temperature
  Temperature must be between 0.0 and 2.0 (type=value_error)
openai_api_key
  field required (type=value_error.missing)
```

## Best Practices

1. **Use environment-specific files**: `.env.development`, `.env.production`
2. **Keep secrets secure**: Never commit API keys to version control
3. **Start with defaults**: Only override what you need to change
4. **Monitor performance**: Adjust timeouts and limits based on usage
5. **Enable tracing**: Use LangSmith for production monitoring
6. **Use caching**: Enable Redis for better performance
7. **Set appropriate limits**: Configure rate limiting for production

## Configuration Reference

For a complete list of all configuration options with their defaults, see:
- `config.py` - Configuration classes and validation
- `env_example.txt` - Example environment file with all options
- `ARCHITECTURE.md` - System architecture and component relationships

## Support

If you encounter configuration issues:

1. Check the validation errors in the logs
2. Verify your `.env` file syntax
3. Ensure all required fields are set
4. Test with default values first
5. Check the GitHub issues for known problems
