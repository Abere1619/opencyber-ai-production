#!/bin/bash
echo "🛡️  OpenCyber AI Platform - Quick Status"
echo "========================================"
echo ""

# Container status
echo "🏃‍♂️ Running Services:"
printf "%-20s %-12s %s\n" "SERVICE" "STATUS" "PORT"
printf "%-20s %-12s %s\n" "backend" "$(podman inspect opencyber-backend --format '{{.State.Status}}')" "8000"
printf "%-20s %-12s %s\n" "postgres" "$(podman inspect opencyber-db --format '{{.State.Status}}')" "5432"
printf "%-20s %-12s %s\n" "redis" "$(podman inspect opencyber-redis --format '{{.State.Status}}')" "6379"
printf "%-20s %-12s %s\n" "nginx" "$(podman inspect opencyber-nginx --format '{{.State.Status}}' 2>/dev/null || echo "not running")" "8080"
printf "%-20s %-12s %s\n" "grafana" "$(podman inspect opencyber-grafana --format '{{.State.Status}}')" "3000"

echo ""
echo "🔍 Health Checks:"
echo -n "Backend API: "
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Healthy"
else
    echo "❌ Unhealthy"
fi

echo -n "Frontend: "
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Accessible"
else
    echo "❌ Unreachable"
fi

echo -n "Grafana: "
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Accessible"
else
    echo "❌ Unreachable"
fi

echo ""
echo "🚀 Quick Access:"
echo "   Frontend:  http://localhost:8080"
echo "   API Docs:  http://localhost:8000/api/docs"
echo "   Grafana:   http://localhost:3000"
echo "   Metrics:   http://localhost:8000/metrics"
