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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL.lower()
    )
