# Test script for MCP Gateway
import asyncio
import json
import aiohttp
from typing import Dict, Any

class GatewayTester:
    def __init__(self, gateway_url: str = "http://localhost:8090"):
        self.gateway_url = gateway_url
        
    async def test_complete_flow(self):
        """Test the complete gateway flow"""
        print("🚀 Starting MCP Gateway Test")
        
        # Load example OpenAPI spec
        with open("example_openapi_spec.json", "r") as f:
            openapi_spec = json.load(f)
        
        async with aiohttp.ClientSession() as session:
            # 1. Check gateway health
            await self._test_health(session)
            
            # 2. Register OpenAPI service
            await self._test_register_service(session, openapi_spec)
            
            # 3. List services
            await self._test_list_services(session)
            
            # 4. Test chat functionality
            await self._test_chat_functionality(session)
            
        print("✅ All tests completed!")
    
    async def _test_health(self, session: aiohttp.ClientSession):
        """Test health endpoint"""
        print("\n📊 Testing health endpoint...")
        try:
            async with session.get(f"{self.gateway_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data}")
                else:
                    print(f"❌ Health check failed: {response.status}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
    
    async def _test_register_service(self, session: aiohttp.ClientSession, openapi_spec: Dict[str, Any]):
        """Test service registration"""
        print("\n📝 Registering OpenAPI service...")
        
        registration_data = {
            "name": "user_service",
            "openapi_spec": openapi_spec,
            "base_url": "https://jsonplaceholder.typicode.com"
        }
        
        try:
            async with session.post(
                f"{self.gateway_url}/register-service",
                json=registration_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Service registered: {data}")
                else:
                    error_text = await response.text()
                    print(f"❌ Service registration failed: {response.status} - {error_text}")
        except Exception as e:
            print(f"❌ Service registration error: {e}")
    
    async def _test_list_services(self, session: aiohttp.ClientSession):
        """Test listing services"""
        print("\n📋 Listing services...")
        try:
            async with session.get(f"{self.gateway_url}/services") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Services listed: {data}")
                else:
                    print(f"❌ Service listing failed: {response.status}")
        except Exception as e:
            print(f"❌ Service listing error: {e}")
    
    async def _test_chat_functionality(self, session: aiohttp.ClientSession):
        """Test chat functionality with various queries"""
        print("\n💬 Testing chat functionality...")
        
        test_queries = [
            "Can you get me a list of all users?",
            "Get user with ID 1",
            "Show me posts from user 2",
            "What users are available in the system?",
            "Get the first user's information"
        ]
        
        for query in test_queries:
            await self._send_chat_message(session, query)
            await asyncio.sleep(2)  # Small delay between requests
    
    async def _send_chat_message(self, session: aiohttp.ClientSession, message: str):
        """Send a chat message and display response"""
        print(f"\n🤖 Query: {message}")
        
        chat_data = {
            "message": message,
            "session_id": "test_session"
        }
        
        try:
            async with session.post(
                f"{self.gateway_url}/chat",
                json=chat_data
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Response: {data['response']}")
                    if data.get('tools_used'):
                        print(f"🔧 Tools used: {data['tools_used']}")
                else:
                    error_text = await response.text()
                    print(f"❌ Chat failed: {response.status} - {error_text}")
        except Exception as e:
            print(f"❌ Chat error: {e}")

async def main():
    """Main test function"""
    tester = GatewayTester()
    await tester.test_complete_flow()

if __name__ == "__main__":
    print("MCP Gateway Test Suite")
    print("Make sure the gateway server is running on localhost:8090")
    print("Start it with: python gateway_server.py")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
