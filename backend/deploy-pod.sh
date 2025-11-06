#!/bin/bash
set -e

echo "🚀 Deploying OpenCyber AI Platform using Podman Pod..."

# Set environment variables
export DB_PASSWORD="opencyber_prod_password_123!"
export SECRET_KEY="your_very_secure_secret_key_change_this_in_production_123!"
export GRAFANA_PASSWORD="grafana_admin_123!"

# Clean up
podman pod stop opencyber-pod 2>/dev/null || true
podman pod rm opencyber-pod 2>/dev/null || true
podman stop -a 2>/dev/null || true
podman rm -a 2>/dev/null || true

# Create volumes
podman volume create postgres_data 2>/dev/null || true
podman volume create redis_data 2>/dev/null || true
podman volume create grafana_data 2>/dev/null || true

# Build backend
echo "Building backend image..."
podman build -t opencyber-backend .

# Create a pod (like a mini-Kubernetes pod)
echo "Creating pod..."
podman pod create --name opencyber-pod -p 8000:8000 -p 8080:80 -p 3000:3000

# Start PostgreSQL in the pod
echo "Starting PostgreSQL..."
podman run -d --pod opencyber-pod \
    --name opencyber-db \
    -e POSTGRES_DB=opencyber_ai \
    -e POSTGRES_USER=opencyber \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -v postgres_data:/var/lib/postgresql/data \
    docker.io/postgres:13

# Start Redis in the pod
echo "Starting Redis..."
podman run -d --pod opencyber-pod \
    --name opencyber-redis \
    -v redis_data:/data \
    docker.io/redis:7-alpine redis-server --appendonly yes

# Wait for database
sleep 10

# Start Backend in the pod
echo "Starting Backend..."
podman run -d --pod opencyber-pod \
    --name opencyber-backend \
    -e DATABASE_URL=postgresql://opencyber:$DB_PASSWORD@localhost:5432/opencyber_ai \
    -e REDIS_URL=redis://localhost:6379 \
    -e SECRET_KEY=$SECRET_KEY \
    -e ENVIRONMENT=production \
    localhost/opencyber-backend

# Start NGINX in the pod
echo "Starting NGINX..."
podman run -d --pod opencyber-pod \
    --name opencyber-nginx \
    -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
    -v ../frontend:/usr/share/nginx/html:ro \
    docker.io/nginx:1.21-alpine

# Start Grafana in the pod
echo "Starting Grafana..."
podman run -d --pod opencyber-pod \
    --name opencyber-grafana \
    -e GF_SECURITY_ADMIN_PASSWORD=$GRAFANA_PASSWORD \
    -v grafana_data:/var/lib/grafana \
    docker.io/grafana/grafana:9.0.0

echo "⏳ Waiting for startup..."
sleep 20

echo "🔍 Testing deployment..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    podman logs opencyber-backend
fi

echo ""
echo "🎉 Pod deployment complete!"
echo "📊 Access URLs:"
echo "   Backend:  http://localhost:8000"
echo "   Frontend: http://localhost:8080"
echo "   Grafana:  http://localhost:3000"
echo ""
echo "🔧 Pod management:"
echo "   View pod:    podman pod ps"
echo "   Stop pod:    podman pod stop opencyber-pod"
echo "   Start pod:   podman pod start opencyber-pod"
echo "   View logs:   podman logs -f opencyber-backend"
