#!/bin/bash

# MCP Gateway Setup Script
echo "🚀 Setting up MCP Gateway..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.13+ and try again."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker and try again."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Install root dependencies
echo "📦 Installing root dependencies..."
npm install

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd packages/frontend
npm install
cd ../..

# Install backend dependencies
echo "🐍 Installing backend dependencies..."
cd packages/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ../..

# Create environment files
echo "⚙️ Setting up environment files..."

# Frontend environment
if [ ! -f packages/frontend/.env ]; then
    cp packages/frontend/env.example packages/frontend/.env
    echo "✅ Created frontend .env file"
fi

# Backend environment
if [ ! -f packages/backend/.env ]; then
    cat > packages/backend/.env << EOF
OPENAI_API_KEY=your_openai_api_key_here
KEYCLOAK_SERVER_URL=http://localhost:1010
KEYCLOAK_REALM=mcp-gateway
KEYCLOAK_CLIENT_ID=mcp-gateway-backend
GATEWAY_HOST=0.0.0.0
GATEWAY_PORT=8090
LOG_LEVEL=INFO
EOF
    echo "✅ Created backend .env file"
fi

# Root environment for Docker
if [ ! -f .env ]; then
    cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
EOF
    echo "✅ Created root .env file"
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Add your OpenAI API key to the .env files"
echo "2. Start the development servers:"
echo "   npm run dev"
echo ""
echo "🐳 Or use Docker:"
echo "   docker-compose -f docker-compose.full.yml up --build"
echo ""
echo "🌐 Access points:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8090"
echo "   - Keycloak: http://localhost:1010"
echo ""
echo "📚 Documentation: See README.md for detailed instructions"
