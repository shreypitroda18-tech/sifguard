import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base

class SafetyReport(Base):
    __tablename__ = "safety_reports"

    id = Column(Integer, primary_key=True, index=True)
    reportId = Column(String, unique=True, index=True)
    reportType = Column(String, index=True) # Unsafe Act, Unsafe Condition, Near Miss, Incident
    title = Column(String)
    description = Column(Text)
    originalLanguage = Column(String, default="English")
    detectedLanguage = Column(String, default="English")
    site = Column(String, index=True)
    location = Column(String)
    department = Column(String, index=True)
    activity = Column(String)
    reportedBy = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    severity = Column(String)
    status = Column(String, default="Open")
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    analysis = relationship("AIAnalysis", back_populates="report", uselist=False)
    actions = relationship("CorrectiveAction", back_populates="report")

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("safety_reports.id"))
    sifDetected = Column(Boolean, default=False)
    confidence = Column(Float)
    riskScore = Column(Integer)
    riskLevel = Column(String) # Low, Medium, High, Critical
    hazardCategories = Column(JSON) # List of hazards
    detectedEntities = Column(JSON) # Evidence
    potentialConsequences = Column(JSON)
    missingControls = Column(JSON)
    recommendations = Column(JSON)
    modelVersion = Column(String, default="demo-nlp-v1")
    analyzedAt = Column(DateTime, default=datetime.datetime.utcnow)

    report = relationship("SafetyReport", back_populates="analysis")

class CorrectiveAction(Base):
    __tablename__ = "corrective_actions"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("safety_reports.id"))
    title = Column(String)
    description = Column(Text)
    priority = Column(String) # Low, Medium, High, Critical
    assignedTo = Column(String)
    department = Column(String)
    dueDate = Column(DateTime)
    status = Column(String, default="Open") # Open, Assigned, In Progress, Pending Verification, Completed, Verified
    createdAt = Column(DateTime, default=datetime.datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    report = relationship("SafetyReport", back_populates="actions")
