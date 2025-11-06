#!/bin/bash

case "$1" in
    start)
        echo "🚀 Starting AbEthiopia Platform..."
        podman start opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana
        echo "✅ Platform started"
        ;;
    stop)
        echo "🛑 Stopping AbEthiopia Platform..."
        podman stop opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana
        echo "✅ Platform stopped"
        ;;
    restart)
        echo "🔄 Restarting AbEthiopia Platform..."
        podman stop opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana
        podman start opencyber-db opencyber-redis opencyber-backend opencyber-nginx opencyber-grafana
        echo "✅ Platform restarted"
        ;;
    status)
        echo "🛡️  AbEthiopia Platform - Status"
        echo "================================"
        echo ""
        podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ;;
    logs)
        echo "📋 Container logs:"
        podman logs "$2" 2>/dev/null || echo "Usage: $0 logs [container-name]"
        ;;
    *)
        echo "AbEthiopia Cyber Intelligence Platform Management"
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Containers: opencyber-db, opencyber-redis, opencyber-backend, opencyber-nginx, opencyber-grafana"
        echo ""
        echo "Access URLs:"
        echo "  Main App:  http://localhost:8080"
        echo "  API Docs:  http://localhost:8000/api/docs"
        echo "  Dashboard: http://localhost:3000 (abere/Sudo12)"
        ;;
esac
