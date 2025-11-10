from app.network_scanner import NetworkScanner
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import uuid
from prometheus_client import Counter, Histogram, generate_latest
from fastapi import Response

from app.core.config import settings
from app.core.database import engine, Base

# Metrics
REQUESTS_TOTAL = Counter(
    'opencyber_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code']
)

THREAT_ANALYSES = Counter(
    'opencyber_threat_analyses_total',
    'Total number of threat analyses',
    ['analysis_type', 'verdict']
)

# Track startup time
startup_time = time.time()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Try to create tables, but don't fail if database is not available
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("⚠️  Starting without database...")
    yield
    # Shutdown
    print("🛑 Application shutting down")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Open-source AI-powered threat intelligence platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "OpenCyber AI Platform API",
        "version": "1.0.0",
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "database": "connected"  # This would be dynamic in real implementation
    }

@app.get("/health")
async def health_check():
    uptime = time.time() - startup_time
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "uptime_seconds": uptime,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

# Simple analysis endpoints for demo
@app.post("/api/v1/analysis/file")
async def analyze_file(file: UploadFile = File(...)):
    THREAT_ANALYSES.labels(analysis_type="file", verdict="clean").inc()
    
    return {
        "analysis_id": str(uuid.uuid4()),
        "verdict": "clean",
        "risk_level": "low",
        "confidence_score": 0.95,
        "processing_time": 0.5,
        "threats_detected": [],
        "ai_engines_used": ["tensorflow", "pytorch"],
        "tensorflow_analysis": {"confidence": 0.95},
        "pytorch_analysis": {"confidence": 0.92}
    }

@app.post("/api/v1/analysis/url")
async def analyze_url(data: dict):
    THREAT_ANALYSES.labels(analysis_type="url", verdict="suspicious").inc()
    
    return {
        "analysis_id": str(uuid.uuid4()),
        "verdict": "suspicious",
        "risk_level": "medium",
        "confidence_score": 0.75,
        "processing_time": 0.3,
        "threats_detected": [
            {
                "type": "Phishing URL",
                "severity": "Medium",
                "confidence": 0.75,
                "description": "URL contains common phishing keywords"
            }
        ],
        "ai_engines_used": ["tensorflow", "pytorch"],
        "tensorflow_analysis": {"confidence": 0.75},
        "pytorch_analysis": {"confidence": 0.72}
    }

@app.post("/api/v1/analysis/ip")
async def analyze_ip(data: dict):
    THREAT_ANALYSES.labels(analysis_type="ip", verdict="malicious").inc()
    
    return {
        "analysis_id": str(uuid.uuid4()),
        "verdict": "malicious",
        "risk_level": "critical",
        "confidence_score": 0.88,
        "processing_time": 0.4,
        "threats_detected": [
            {
                "type": "Malware Distribution",
                "severity": "Critical",
                "confidence": 0.88,
                "description": "IP associated with malware distribution"
            }
        ],
        "ai_engines_used": ["pytorch", "opencti"],
        "pytorch_analysis": {"confidence": 0.88},
        "opencti_analysis": {"threat_count": 1}
    }

@app.get("/api/v1/dashboard/stats")
async def get_dashboard_stats():
    return {
        "total_threats_analyzed": 12847,
        "threats_today": 42,
        "detection_accuracy": 99.1,
        "average_processing_time": 0.35,
        "system_status": "healthy",
        "active_models": ["tensorflow", "pytorch", "opencti", "misp"]
    }

@app.post("/api/v1/network/scan")
async def network_scan(ip_request: dict):
    """
    Network scanning endpoint for IP reconnaissance
    """
    try:
        scanner = NetworkScanner()
        ip_address = ip_request.get("ip", "").strip()
        
        if not ip_address:
            return {"error": "IP address required"}
        
        scan_results = scanner.scan_ip(ip_address)
        
        if "error" in scan_results:
            return scan_results
            
        threat_assessment = assess_network_threat(scan_results)
        scan_results["threat_assessment"] = threat_assessment
        
        return scan_results
        
    except Exception as e:
        return {"error": f"Scan failed: {str(e)}"}

def assess_network_threat(scan_results: dict) -> dict:
    threat_score = 0
    warnings = []
    
    if scan_results.get("reachable"):
        threat_score += 10
    
    open_ports = scan_results.get("open_ports", [])
    suspicious_ports = [23, 135, 139, 445, 1433, 3389]
    
    for port_info in open_ports:
        port = port_info["port"]
        if port in suspicious_ports:
            threat_score += 20
            warnings.append(f"Suspicious port open: {port} ({port_info['service']})")
        else:
            threat_score += 5
    
    if threat_score >= 30:
        level = "High"
    elif threat_score >= 15:
        level = "Medium"
    else:
        level = "Low"
    
    return {
        "threat_score": threat_score,
        "level": level,
        "warnings": warnings,
        "open_port_count": len(open_ports)
    }


@app.get("/api/v1/threat-intel/feeds")
async def get_threat_intel_feeds():
    """
    Get available threat intelligence feeds
    """
    return {
        "ethiopian_organizations": {
            "financial": [
                "cbe.et", "dbee.et", "awashbank.com", "dashenbanksc.com", 
                "nibbank.com", "unitybank.com", "abyssiniabank.com"
            ],
            "government": [
                "gov.et", "mfa.gov.et", "mofed.gov.et", "moh.gov.et",
                "ethio telecom", "ethiopian airlines", "eea.gov.et"
            ],
            "telecom": [
                "ethiotelecom.et", "telecom.et", "ethiotelecom.com.et"
            ],
            "critical_infrastructure": [
                "eep.com.et", "eeu.gov.et", "ethiopianairlines.com"
            ]
        },
        "international_feeds": [
            "OpenPhish",
            "URLhaus", 
            "Phishing Database",
            "AbuseIPDB",
            "VirusTotal"
        ],
        "ai_engines": [
            "TensorFlow",
            "PyTorch", 
            "OpenCTI",
            "Static Analysis"
        ],
        "last_updated": "2024-01-10",
        "status": "operational"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    )

# Add this import at the top with other imports
from app.network_scanner import NetworkScanner

# Add this route with your existing API endpoints
@app.post("/api/v1/network/scan")
async def network_scan(ip_request: dict):
    """
    Network scanning endpoint for IP reconnaissance
    """
    try:
        scanner = NetworkScanner()
        ip_address = ip_request.get("ip", "").strip()
        
        if not ip_address:
            return {"error": "IP address required"}
        
        # Perform network scan
        scan_results = scanner.scan_ip(ip_address)
        
        # Enhanced threat assessment based on scan results
        threat_assessment = assess_network_threat(scan_results)
        scan_results["threat_assessment"] = threat_assessment
        
        return scan_results
        
    except Exception as e:
        return {"error": f"Scan failed: {str(e)}"}

def assess_network_threat(scan_results: dict) -> dict:
    """
    Assess threat level based on network scan results
    """
    threat_score = 0
    warnings = []
    
    if scan_results.get("reachable"):
        threat_score += 10
    
    open_ports = scan_results.get("open_ports", [])
    suspicious_ports = [23, 135, 139, 445, 1433, 3389]  # Common attack vectors
    
    for port_info in open_ports:
        port = port_info["port"]
        if port in suspicious_ports:
            threat_score += 20
            warnings.append(f"Suspicious port open: {port} ({port_info['service']})")
        else:
            threat_score += 5
    
    # Determine threat level
    if threat_score >= 30:
        level = "High"
    elif threat_score >= 15:
        level = "Medium"
    else:
        level = "Low"
    
    return {
        "threat_score": threat_score,
        "level": level,
        "warnings": warnings,
        "open_port_count": len(open_ports)
    }

# Add this import at the top with other imports
from app.network_scanner import NetworkScanner

# Add this route with your existing API endpoints
@app.post("/api/v1/network/scan")
async def network_scan(ip_request: dict):
    """
    Network scanning endpoint for IP reconnaissance
    """
    try:
        scanner = NetworkScanner()
        ip_address = ip_request.get("ip", "").strip()
        
        if not ip_address:
            return {"error": "IP address required"}
        
        # Perform network scan
        scan_results = scanner.scan_ip(ip_address)
        
        # Enhanced threat assessment based on scan results
        threat_assessment = assess_network_threat(scan_results)
        scan_results["threat_assessment"] = threat_assessment
        
        return scan_results
        
    except Exception as e:
        return {"error": f"Scan failed: {str(e)}"}

def assess_network_threat(scan_results: dict) -> dict:
    """
    Assess threat level based on network scan results
    """
    threat_score = 0
    warnings = []
    
    if scan_results.get("reachable"):
        threat_score += 10
    
    open_ports = scan_results.get("open_ports", [])
    suspicious_ports = [23, 135, 139, 445, 1433, 3389]  # Common attack vectors
    
    for port_info in open_ports:
        port = port_info["port"]
        if port in suspicious_ports:
            threat_score += 20
            warnings.append(f"Suspicious port open: {port} ({port_info['service']})")
        else:
            threat_score += 5
    
    # Determine threat level
    if threat_score >= 30:
        level = "High"
    elif threat_score >= 15:
        level = "Medium"
    else:
        level = "Low"
    
    return {
        "threat_score": threat_score,
        "level": level,
        "warnings": warnings,
        "open_port_count": len(open_ports)
    }

# Add threat intelligence import
from app.threat_intelligence import ThreatIntelligence

@app.post("/api/v1/analysis/url")
async def analyze_url(url_request: dict):
    """
    Enhanced URL analysis with Ethiopian organizational context
    """
    try:
        threat_intel = ThreatIntelligence()
        url = url_request.get("url", "").strip()
        
        if not url:
            return {"error": "URL is required"}
        
        # Perform comprehensive analysis
        analysis = threat_intel.analyze_url(url)
        
        return analysis
        
    except Exception as e:
        return {"error": f"URL analysis failed: {str(e)}"}

@app.post("/api/v1/analysis/ip")
async def analyze_ip(ip_request: dict):
    """
    Enhanced IP analysis with Ethiopian context
    """
    try:
        threat_intel = ThreatIntelligence()
        ip_address = ip_request.get("ip", "").strip()
        
        if not ip_address:
            return {"error": "IP address is required"}
        
        # Perform comprehensive analysis
        analysis = threat_intel.analyze_ip(ip_address)
        
        return analysis
        
    except Exception as e:
        return {"error": f"IP analysis failed: {str(e)}"}

@app.post("/api/v1/analysis/file")
async def analyze_file(file_request: dict = None, file: UploadFile = None):
    """
    Enhanced file analysis with multi-engine detection
    """
    try:
        threat_intel = ThreatIntelligence()
        
        if file:
            # Handle file upload
            file_data = await file.read()
            filename = file.filename
            
            analysis = threat_intel.analyze_file(file_data, filename)
            return analysis
        else:
            return {"error": "File is required"}
        
    except Exception as e:
        return {"error": f"File analysis failed: {str(e)}"}

@app.get("/api/v1/threat-intel/feeds")
async def get_threat_feeds():
    """
    Get available threat intelligence feeds
    """
    threat_intel = ThreatIntelligence()
    return {
        "ethiopian_organizations": threat_intel.ethiopian_orgs,
        "international_feeds": list(threat_intel.threat_feeds.keys()),
        "last_updated": "2024-01-10"
    }

@app.get("/api/v1/threat-intel/feeds")
async def get_threat_intel_feeds():
    """
    Get available threat intelligence feeds
    """
    return {
        "ethiopian_organizations": {
            "financial": [
                "cbe.et", "dbee.et", "awashbank.com", "dashenbanksc.com", 
                "nibbank.com", "unitybank.com", "abyssiniabank.com"
            ],
            "government": [
                "gov.et", "mfa.gov.et", "mofed.gov.et", "moh.gov.et",
                "ethio telecom", "ethiopian airlines", "eea.gov.et"
            ],
            "telecom": [
                "ethiotelecom.et", "telecom.et", "ethiotelecom.com.et"
            ],
            "critical_infrastructure": [
                "eep.com.et", "eeu.gov.et", "ethiopianairlines.com"
            ]
        },
        "international_feeds": [
            "OpenPhish",
            "URLhaus", 
            "Phishing Database",
            "AbuseIPDB",
            "VirusTotal"
        ],
        "ai_engines": [
            "TensorFlow",
            "PyTorch", 
            "OpenCTI",
            "Static Analysis"
        ],
        "last_updated": "2024-01-10",
        "status": "operational"
    }
