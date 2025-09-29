# Simple test client to verify MCP connection
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_connection():
    server_params = StdioServerParameters(
        command="python3",
        args=["/Users/syed.afroz/work/mcp/mcp-lc/math_server.py"],
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize the connection
                await session.initialize()
                print("✅ Successfully connected to MCP server")
                
                # List available tools
                tools_response = await session.list_tools()
                print(f"✅ Available tools: {[tool.name for tool in tools_response.tools]}")
                
                # Test calling a tool
                result = await session.call_tool("add", {"a": 3, "b": 5})
                print(f"✅ Tool call result: add(3, 5) = {result.content}")
                
                # Test another tool
                result = await session.call_tool("multiply", {"a": 8, "b": 12})
                print(f"✅ Tool call result: multiply(8, 12) = {result.content}")
                
    except Exception as e:
        import traceback
        print(f"❌ Error: {e}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())
