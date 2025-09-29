# math_server.py
import sys
from mcp.server.fastmcp import FastMCP

print("Starting math server...", file=sys.stderr)
mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"Adding {a} + {b}", file=sys.stderr)
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print(f"Multiplying {a} * {b}", file=sys.stderr)
    return a * b

if __name__ == "__main__":
    print("Running MCP server with stdio transport...", file=sys.stderr)
    mcp.run(transport="stdio")