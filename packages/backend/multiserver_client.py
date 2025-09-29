import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

 # Load environment variables from .env file
load_dotenv()

client = MultiServerMCPClient(
    {
        "math": {
            "command": "python3",
            # Make sure to update to the full absolute path to your math_server.py file
            "args": ["/Users/syed.afroz/work/mcp/mcp-lc/math_server.py"],
            "transport": "stdio",
        },
        "weather": {
            # Make sure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp/",
            "transport": "streamable_http",
        }
    }
)

async def main():
    tools = await client.get_tools()
    agent = create_react_agent("openai:gpt-4.1", tools)
    math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
    print(math_response)

    weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
    print(weather_response)

if __name__ == "__main__":
    asyncio.run(main())