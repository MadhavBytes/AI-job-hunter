#!/bin/bash
# Auto-apply deployment script for AI Job Hunter
set -e
echo "Starting AI Job Hunter deployment..."

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

# Build and start services
echo "Building Docker images and starting services..."
docker-compose down || true
docker-compose up -d --build

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check service health
echo "Checking service health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/jobs > /dev/null 2>&1; then
        echo "Backend is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "Backend failed to start"
        exit 1
    fi
    sleep 1
done

echo "Backend is running on http://localhost:8000"
echo "Frontend is running on http://localhost:3000"
echo "Deployment complete!"
