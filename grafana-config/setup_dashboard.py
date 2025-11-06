import json
import requests
import time

# Wait for Grafana to be ready
time.sleep(30)

dashboard = {
    "dashboard": {
        "id": None,
        "title": "🇪🇹 ABETHIOPIA CYBER INTELLIGENCE PLATFORM",
        "tags": ["cybersecurity", "threat-intel", "ab-ethiopia"],
        "timezone": "browser",
        "panels": [
            {
                "id": 1,
                "type": "text",
                "title": "",
                "gridPos": {"h": 6, "w": 24, "x": 0, "y": 0},
                "mode": "markdown",
                "content": "# 🦅 ABETHIOPIA CYBER INTELLIGENCE PLATFORM\n\n## Enterprise Threat Detection & Monitoring\n\n**🇪🇹 Protecting Ethiopian Digital Infrastructure**\n\n### Core Features:\n- 🔍 **File Malware Analysis**\n- 🌐 **URL Phishing Detection**\n- 📡 **IP Threat Intelligence**\n- 🤖 **Multi-AI Engine Analysis**\n- 📊 **Real-time Monitoring**"
            }
        ],
        "time": {"from": "now-6h", "to": "now"},
        "refresh": "30s"
    },
    "overwrite": True
}

print("Dashboard JSON ready to be imported")
print(json.dumps(dashboard, indent=2))
