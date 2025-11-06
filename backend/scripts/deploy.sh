#!/bin/bash

set -e

echo "🚀 Starting OpenCyber AI Platform deployment..."

# Load environment variables
if [ -f .env.production ]; then
    export $(cat .env.production | grep -v '^#' | xargs)
else
    echo "❌ .env.production file not found!"
    exit 1
fi

# Build and start services
echo "Building and starting services..."
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 30

# Check if backend is healthy
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose -f docker-compose.prod.yml logs backend
    exit 1
fi

echo "🎉 Deployment completed successfully!"
echo ""
echo "📊 Access your platform:"
echo "   Frontend: http://localhost"
echo "   API: http://localhost/api/docs"
echo "   Monitoring: http://localhost:3000 (admin/${GRAFANA_PASSWORD})"
echo ""
echo "💡 To view logs: docker-compose -f docker-compose.prod.yml logs -f"
