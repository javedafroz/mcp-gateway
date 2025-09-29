#!/bin/bash

# MCP Gateway Docker Runner Script
# This script provides easy commands to manage the MCP Gateway with Docker

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_usage() {
    echo "MCP Gateway Docker Runner"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  dev         Start development environment"
    echo "  prod        Start production environment"
    echo "  test        Run tests in container"
    echo "  build       Build Docker images"
    echo "  stop        Stop all services"
    echo "  clean       Stop and remove all containers, networks, and volumes"
    echo "  logs        Show logs from services"
    echo "  health      Check health of services"
    echo "  shell       Open shell in gateway container"
    echo ""
    echo "Options:"
    echo "  --build     Force rebuild of images"
    echo "  --detach    Run in background (detached mode)"
    echo "  --follow    Follow logs output"
    echo ""
    echo "Examples:"
    echo "  $0 dev --build              # Build and start development environment"
    echo "  $0 prod --detach            # Start production environment in background"
    echo "  $0 logs --follow            # Follow logs from all services"
    echo "  $0 test                     # Run tests"
}

check_env_file() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}Warning: .env file not found${NC}"
        echo "Creating .env file from docker.env.example..."
        
        if [ -f "docker.env.example" ]; then
            cp docker.env.example .env
            echo -e "${YELLOW}Please edit .env file and add your OpenAI API key${NC}"
        else
            echo -e "${RED}Error: docker.env.example not found${NC}"
            exit 1
        fi
    fi
}

wait_for_service() {
    local service_name=$1
    local url=$2
    local max_attempts=30
    local attempt=1

    echo -e "${BLUE}Waiting for $service_name to be ready...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s -f "$url" > /dev/null 2>&1; then
            echo -e "${GREEN}$service_name is ready!${NC}"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo -e "${RED}$service_name failed to start within expected time${NC}"
    return 1
}

# Main script logic
case "${1:-}" in
    "dev")
        echo -e "${BLUE}Starting MCP Gateway in development mode...${NC}"
        check_env_file
        
        COMPOSE_CMD="docker-compose -f docker-compose.dev.yml"
        
        if [[ "$*" == *"--build"* ]]; then
            COMPOSE_CMD="$COMPOSE_CMD --build"
        fi
        
        if [[ "$*" == *"--detach"* ]]; then
            $COMPOSE_CMD up -d
        else
            $COMPOSE_CMD up
        fi
        
        if [[ "$*" == *"--detach"* ]]; then
            wait_for_service "MCP Gateway" "http://localhost:8090/health"
            echo -e "${GREEN}Development environment started!${NC}"
            echo "Gateway: http://localhost:8090"
            echo "API Docs: http://localhost:8090/docs"
        fi
        ;;
        
    "prod")
        echo -e "${BLUE}Starting MCP Gateway in production mode...${NC}"
        check_env_file
        
        COMPOSE_CMD="docker-compose -f docker-compose.prod.yml"
        
        if [[ "$*" == *"--build"* ]]; then
            COMPOSE_CMD="$COMPOSE_CMD --build"
        fi
        
        if [[ "$*" == *"--detach"* ]]; then
            $COMPOSE_CMD up -d
        else
            $COMPOSE_CMD up
        fi
        
        if [[ "$*" == *"--detach"* ]]; then
            wait_for_service "MCP Gateway" "http://localhost:8090/health"
            echo -e "${GREEN}Production environment started!${NC}"
            echo "Gateway: http://localhost:8090"
            echo "Nginx: http://localhost:80"
            echo "API Docs: http://localhost:8090/docs"
        fi
        ;;
        
    "build")
        echo -e "${BLUE}Building Docker images...${NC}"
        docker-compose build
        echo -e "${GREEN}Build completed!${NC}"
        ;;
        
    "stop")
        echo -e "${YELLOW}Stopping all services...${NC}"
        docker-compose -f docker-compose.yml down
        docker-compose -f docker-compose.dev.yml down
        docker-compose -f docker-compose.prod.yml down
        echo -e "${GREEN}All services stopped!${NC}"
        ;;
        
    "clean")
        echo -e "${YELLOW}Cleaning up all Docker resources...${NC}"
        docker-compose -f docker-compose.yml down -v --remove-orphans
        docker-compose -f docker-compose.dev.yml down -v --remove-orphans
        docker-compose -f docker-compose.prod.yml down -v --remove-orphans
        docker system prune -f
        echo -e "${GREEN}Cleanup completed!${NC}"
        ;;
        
    "logs")
        if [[ "$*" == *"--follow"* ]]; then
            docker-compose logs -f
        else
            docker-compose logs
        fi
        ;;
        
    "health")
        echo -e "${BLUE}Checking service health...${NC}"
        
        # Check gateway
        if curl -s -f "http://localhost:8090/health" > /dev/null; then
            echo -e "${GREEN}✓ MCP Gateway: Healthy${NC}"
        else
            echo -e "${RED}✗ MCP Gateway: Unhealthy${NC}"
        fi
        
        # Check Docker containers
        echo ""
        echo "Container Status:"
        docker-compose ps
        ;;
        
    "shell")
        echo -e "${BLUE}Opening shell in gateway container...${NC}"
        docker-compose exec mcp-gateway /bin/bash
        ;;
        
    "test")
        echo -e "${BLUE}Running tests...${NC}"
        check_env_file
        docker-compose -f docker-compose.dev.yml up -d
        
        # Wait for services to be ready
        wait_for_service "MCP Gateway" "http://localhost:8090/health"
        
        # Run tests
        docker-compose -f docker-compose.dev.yml exec mcp-gateway python quick_demo.py
        
        echo -e "${GREEN}Tests completed!${NC}"
        ;;
        
    "help"|"-h"|"--help"|"")
        print_usage
        ;;
        
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        print_usage
        exit 1
        ;;
esac
