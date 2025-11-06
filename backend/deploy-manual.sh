#!/bin/bash
set -e

echo "🚀 Starting manual deployment of OpenCyber AI Platform..."

# Load environment variables
source .env.production

# Create network
docker network create opencyber-network 2>/dev/null || echo "Network already exists"

# Create volumes
docker volume create postgres_data 2>/dev/null || echo "Volume exists"
docker volume create redis_data 2>/dev/null || echo "Volume exists" 
docker volume create opencyber_logs 2>/dev/null || echo "Volume exists"
docker volume create opencyber_uploads 2>/dev/null || echo "Volume exists"
docker volume create grafana_data 2>/dev/null || echo "Volume exists"

# Stop existing containers
docker stop opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana 2>/dev/null || true
docker rm opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana 2>/dev/null || true

# Start PostgreSQL
echo "Starting PostgreSQL..."
docker run -d --name opencyber-db \
    --network opencyber-network \
    -e POSTGRES_DB=opencyber_ai \
    -e POSTGRES_USER=opencyber \
    -e POSTGRES_PASSWORD=${DB_PASSWORD} \
    -v postgres_data:/var/lib/postgresql/data \
    --restart unless-stopped \
    postgres:13

# Start Redis
echo "Starting Redis..."
docker run -d --name opencyber-redis \
    --network opencyber-network \
    -v redis_data:/data \
    --restart unless-stopped \
    redis:7-alpine redis-server --appendonly yes

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Build backend image
echo "Building backend image..."
docker build -t opencyber-backend .

# Start Backend
echo "Starting Backend..."
docker run -d --name opencyber-backend \
    --network opencyber-network \
    -e DATABASE_URL=postgresql://opencyber:${DB_PASSWORD}@opencyber-db:5432/opencyber_ai \
    -e REDIS_URL=redis://opencyber-redis:6379 \
    -e SECRET_KEY=${SECRET_KEY} \
    -e ENVIRONMENT=production \
    -v opencyber_logs:/app/logs \
    -v opencyber_uploads:/app/uploads \
    --restart unless-stopped \
    opencyber-backend

# Start NGINX
echo "Starting NGINX..."
docker run -d --name opencyber-nginx \
    --network opencyber-network \
    -p 80:80 \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf \
    -v ../frontend:/usr/share/nginx/html \
    --restart unless-stopped \
    nginx:1.21-alpine

# Start Grafana
echo "Starting Grafana..."
docker run -d --name opencyber-grafana \
    --network opencyber-network \
    -p 3000:3000 \
    -e GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD} \
    -v grafana_data:/var/lib/grafana \
    --restart unless-stopped \
    grafana/grafana:9.0.0

echo "Waiting for services to start..."
sleep 20

# Health check
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Deployment successful!"
    echo ""
    echo "📊 Access your platform:"
    echo "   Frontend: http://localhost"
    echo "   API: http://localhost/api/docs" 
    echo "   Monitoring: http://localhost:3000 (admin: ${GRAFANA_PASSWORD})"
else
    echo "❌ Health check failed"
    echo "Checking backend logs..."
    docker logs opencyber-backend
fi
