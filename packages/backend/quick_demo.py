#!/usr/bin/env python3
"""
Quick Demo Script for MCP Gateway
This script demonstrates the complete workflow of the MCP Gateway.
"""

import asyncio
import json
import aiohttp
import time
from pathlib import Path

async def wait_for_gateway(url: str, max_attempts: int = 30):
    """Wait for gateway to be ready"""
    print("⏳ Waiting for gateway to be ready...")
    
    for attempt in range(max_attempts):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health") as response:
                    if response.status == 200:
                        print("✅ Gateway is ready!")
                        return True
        except:
            pass
        
        await asyncio.sleep(1)
    
    print("❌ Gateway not ready after 30 seconds")
    return False

async def run_complete_demo():
    """Run the complete MCP Gateway demonstration"""
    gateway_url = "http://localhost:8090"
    
    print("🎯 MCP Gateway Complete Demo")
    print("=" * 40)
    
    # Wait for gateway to be ready
    if not await wait_for_gateway(gateway_url):
        print("Please start the gateway first: python start_gateway.py")
        return
    
    # Load example OpenAPI spec
    spec_file = Path("example_openapi_spec.json")
    if not spec_file.exists():
        print("❌ example_openapi_spec.json not found")
        return
    
    with open(spec_file, "r") as f:
        openapi_spec = json.load(f)
    
    async with aiohttp.ClientSession() as session:
        
        # Step 1: Register the service
        print("\n📝 Step 1: Registering User Service")
        print("-" * 30)
        
        registration_data = {
            "name": "user_service",
            "openapi_spec": openapi_spec,
            "base_url": "https://jsonplaceholder.typicode.com"
        }
        
        async with session.post(f"{gateway_url}/register-service", json=registration_data) as response:
            if response.status == 200:
                result = await response.json()
                print(f"✅ Service registered: {result['message']}")
            else:
                error = await response.text()
                print(f"❌ Registration failed: {error}")
                return
        
        # Wait for service to initialize
        print("⏳ Waiting for service to initialize...")
        await asyncio.sleep(3)
        
        # Step 2: List services
        print("\n📋 Step 2: Listing Services")
        print("-" * 30)
        
        async with session.get(f"{gateway_url}/services") as response:
            if response.status == 200:
                services = await response.json()
                print(f"✅ Active services: {services['active_servers']}")
            else:
                print("❌ Failed to list services")
        
        # Step 3: Demo chat interactions
        print("\n💬 Step 3: Chat Demonstrations")
        print("-" * 30)
        
        demo_conversations = [
            {
                "query": "Can you get information about user with ID 1?",
                "description": "Testing user lookup by ID"
            },
            {
                "query": "Show me all users in the system",
                "description": "Testing user listing"
            },
            {
                "query": "Get posts written by user 2",
                "description": "Testing posts with user filter"
            },
            {
                "query": "What's the name and email of user 3?",
                "description": "Testing specific user data extraction"
            }
        ]
        
        for i, demo in enumerate(demo_conversations, 1):
            print(f"\n🔍 Demo {i}: {demo['description']}")
            print(f"❓ User: {demo['query']}")
            
            chat_data = {
                "message": demo['query'],
                "session_id": f"demo_session_{i}"
            }
            
            start_time = time.time()
            async with session.post(f"{gateway_url}/chat", json=chat_data) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    result = await response.json()
                    print(f"🤖 Assistant: {result['response']}")
                    if result.get('tools_used'):
                        print(f"🔧 Tools used: {', '.join(result['tools_used'])}")
                    print(f"⏱️  Response time: {response_time:.2f}s")
                else:
                    error = await response.text()
                    print(f"❌ Chat failed: {error}")
            
            # Small delay between demos
            await asyncio.sleep(2)
        
        # Step 4: Show final status
        print(f"\n📊 Step 4: Final Status")
        print("-" * 30)
        
        async with session.get(f"{gateway_url}/health") as response:
            if response.status == 200:
                health = await response.json()
                print(f"✅ Gateway healthy with {health['services']} services")
        
        print("\n🎉 Demo completed successfully!")
        print("\nYou can now:")
        print("  - Register more services with different OpenAPI specs")
        print("  - Chat with the gateway using the /chat endpoint")
        print("  - View API docs at http://localhost:8090/docs")

def main():
    """Main demo function"""
    print("Starting MCP Gateway Demo...")
    print("Make sure the gateway is running: python start_gateway.py")
    print()
    
    try:
        asyncio.run(run_complete_demo())
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Make sure:")
        print("1. Gateway is running (python start_gateway.py)")
        print("2. OpenAI API key is set")
        print("3. Internet connection is available")

if __name__ == "__main__":
    main()
