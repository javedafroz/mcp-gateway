# Example usage of MCP Gateway
import asyncio
import json
import aiohttp

async def demo_gateway_usage():
    """Demonstrate how to use the MCP Gateway"""
    
    # Load the example OpenAPI specification
    with open("example_openapi_spec.json", "r") as f:
        openapi_spec = json.load(f)
    
    gateway_url = "http://localhost:8090"
    
    async with aiohttp.ClientSession() as session:
        print("🚀 MCP Gateway Demo")
        
        # 1. Register the user service from OpenAPI spec
        print("\n📝 Registering User Service...")
        registration_data = {
            "name": "user_service",
            "openapi_spec": openapi_spec,
            "base_url": "https://jsonplaceholder.typicode.com"
        }
        
        async with session.post(f"{gateway_url}/register-service", json=registration_data) as response:
            result = await response.json()
            print(f"✅ {result}")
        
        # Wait a moment for the service to fully initialize
        await asyncio.sleep(2)
        
        # 2. Now use the chat interface to interact with the API
        print("\n💬 Using Chat Interface...")
        
        chat_queries = [
            "Get me information about user with ID 1",
            "Show me all users in the system", 
            "Get posts from user ID 2",
            "What information do you have about users?"
        ]
        
        for query in chat_queries:
            print(f"\n🤖 User: {query}")
            
            chat_data = {
                "message": query,
                "session_id": "demo_session"
            }
            
            async with session.post(f"{gateway_url}/chat", json=chat_data) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"🤖 Assistant: {data['response']}")
                    if data.get('tools_used'):
                        print(f"🔧 Tools used: {', '.join(data['tools_used'])}")
                else:
                    print(f"❌ Error: {response.status}")
            
            await asyncio.sleep(1)  # Small delay between requests

if __name__ == "__main__":
    print("Make sure to start the gateway server first:")
    print("python gateway_server.py")
    print("\nThen run this demo script to see it in action!")
    
    try:
        asyncio.run(demo_gateway_usage())
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure the gateway server is running and you have set your OPENAI_API_KEY")
