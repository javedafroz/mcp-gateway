#!/usr/bin/env python3
"""
Startup script for MCP Gateway
This script helps set up and start the MCP Gateway with proper environment checks.
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def check_requirements():
    """Check if all requirements are installed"""
    print("🔍 Checking requirements...")
    
    required_packages = [
        "fastapi", "uvicorn", "aiohttp", "pydantic", 
        "mcp", "langchain-mcp-adapters", "langgraph"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ Packages installed successfully")
    else:
        print("✅ All requirements satisfied")

def check_environment():
    """Check environment variables"""
    print("\n🌍 Checking environment...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not found in environment")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print("Or create a .env file with: OPENAI_API_KEY=your-api-key-here")
        
        # Try to load from .env file
        env_file = Path(".env")
        if env_file.exists():
            print("📄 Found .env file, loading environment variables...")
            from dotenv import load_dotenv
            load_dotenv()
            if os.getenv("OPENAI_API_KEY"):
                print("✅ OpenAI API key loaded from .env file")
            else:
                print("❌ OpenAI API key not found in .env file")
                return False
        else:
            return False
    else:
        print("✅ OpenAI API key found")
    
    return True

def start_gateway():
    """Start the MCP Gateway server"""
    print("\n🚀 Starting MCP Gateway...")
    print("Gateway will be available at: http://localhost:8090")
    print("Press Ctrl+C to stop the server")
    print("\nEndpoints:")
    print("  - POST /register-service  - Register new API service")
    print("  - POST /chat             - Chat with registered services") 
    print("  - GET  /services         - List registered services")
    print("  - GET  /health           - Health check")
    print("  - GET  /docs             - API documentation")
    print("\n" + "="*50)
    
    try:
        # Import and run the gateway
        import uvicorn
        uvicorn.run(
            "gateway_server:app",
            host="0.0.0.0",
            port=8090,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Gateway stopped by user")
    except Exception as e:
        print(f"❌ Failed to start gateway: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    print("🏗️  MCP Gateway Startup")
    print("=" * 30)
    
    # Check requirements
    try:
        check_requirements()
    except Exception as e:
        print(f"❌ Requirements check failed: {e}")
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please set up your OpenAI API key and try again.")
        sys.exit(1)
    
    # Start the gateway
    start_gateway()

if __name__ == "__main__":
    main()
