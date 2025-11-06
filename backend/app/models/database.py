from sqlalchemy import Column, String, Integer, DateTime, Boolean, Float, JSON, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class ThreatAnalysis(Base):
    __tablename__ = "threat_analyses"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    analysis_type = Column(String(50), nullable=False)
    target = Column(Text, nullable=False)
    file_hash_md5 = Column(String(32), nullable=True)
    file_hash_sha256 = Column(String(64), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(100), nullable=True)
    
    verdict = Column(String(20), nullable=False)
    risk_level = Column(String(20), nullable=False)
    confidence_score = Column(Float, nullable=False)
    
    tensorflow_result = Column(JSON, nullable=True)
    pytorch_result = Column(JSON, nullable=True)
    opencti_result = Column(JSON, nullable=True)
    misp_result = Column(JSON, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processing_time = Column(Float, nullable=True)

class SystemMetrics(Base):
    __tablename__ = "system_metrics"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    threats_analyzed = Column(Integer, default=0)
    threats_analyzed_today = Column(Integer, default=0)
    average_processing_time = Column(Float, default=0.0)
    detection_accuracy = Column(Float, default=0.0)
    
    active_models = Column(JSON, nullable=True)
    system_status = Column(String(20), default="healthy")
