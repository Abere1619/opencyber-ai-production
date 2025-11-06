#!/bin/bash
set -e

echo "🚀 Deploying OpenCyber AI Platform with Podman..."

# Set environment variables
export DB_PASSWORD="opencyber_prod_password_123!"
export SECRET_KEY="your_very_secure_secret_key_change_this_in_production_123!"
export GRAFANA_PASSWORD="grafana_admin_123!"

# Clean up any existing containers
echo "Cleaning up existing containers..."
podman stop -a 2>/dev/null || true
podman rm -a 2>/dev/null || true

# Create volumes
echo "Creating volumes..."
podman volume create postgres_data 2>/dev/null || echo "Postgres volume exists"
podman volume create redis_data 2>/dev/null || echo "Redis volume exists"
podman volume create grafana_data 2>/dev/null || echo "Grafana volume exists"

# Create network
echo "Creating network..."
podman network create opencyber-network 2>/dev/null || echo "Network exists"

# Build the backend image
echo "Building backend image..."
podman build -t opencyber-backend .

# Start PostgreSQL
echo "Starting PostgreSQL..."
podman run -d --name opencyber-db \
    --network opencyber-network \
    -e POSTGRES_DB=opencyber_ai \
    -e POSTGRES_USER=opencyber \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -v postgres_data:/var/lib/postgresql/data \
    docker.io/postgres:13

# Start Redis
echo "Starting Redis..."
podman run -d --name opencyber-redis \
    --network opencyber-network \
    -v redis_data:/data \
    docker.io/redis:7-alpine redis-server --appendonly yes

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 15

# Start Backend
echo "Starting Backend..."
podman run -d --name opencyber-backend \
    --network opencyber-network \
    -p 8000:8000 \
    -e DATABASE_URL=postgresql://opencyber:$DB_PASSWORD@opencyber-db:5432/opencyber_ai \
    -e REDIS_URL=redis://opencyber-redis:6379 \
    -e SECRET_KEY=$SECRET_KEY \
    -e ENVIRONMENT=production \
    localhost/opencyber-backend

# Start NGINX
echo "Starting NGINX..."
podman run -d --name opencyber-nginx \
    --network opencyber-network \
    -p 8080:80 \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
    -v ../frontend:/usr/share/nginx/html:ro \
    docker.io/nginx:1.21-alpine

# Start Grafana
echo "Starting Grafana..."
podman run -d --name opencyber-grafana \
    --network opencyber-network \
    -p 3000:3000 \
    -e GF_SECURITY_ADMIN_PASSWORD=$GRAFANA_PASSWORD \
    -v $(pwd)/grafana-config/custom.ini:/etc/grafana/grafana.ini:ro \
    -v grafana_data:/var/lib/grafana \
    docker.io/grafana/grafana:9.0.0

echo "⏳ Waiting for services to start..."
sleep 25

# Check deployment status
echo "🔍 Checking deployment status..."
echo "Containers:"
podman ps

echo ""
echo "🧪 Testing services..."

# Test backend directly
echo "Backend health check:"
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    echo "Backend logs:"
    podman logs opencyber-backend
fi

# Test through nginx
echo "NGINX health check:"
if curl -s http://localhost:8080/health > /dev/null; then
    echo "✅ NGINX is routing properly"
else
    echo "⚠️  NGINX routing test failed (might need more time)"
fi

echo ""
echo "🎉 OpenCyber AI Platform Deployment Complete!"
echo ""
echo "📊 Access URLs:"
echo "   Backend API:    http://localhost:8000"
echo "   Frontend:       http://localhost:8080"
echo "   API Documentation: http://localhost:8000/api/docs"
echo "   Monitoring:     http://localhost:3000"
echo "   Grafana Login:  admin / $GRAFANA_PASSWORD"
echo ""
echo "🔧 Management Commands:"
echo "   View logs:      podman logs -f opencyber-backend"
echo "   View all containers: podman ps -a"
echo "   Stop platform:  podman stop opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana"
echo "   Start platform: podman start opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana"
