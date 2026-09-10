from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class CorrectiveActionBase(BaseModel):
    title: str
    description: str
    priority: str
    assignedTo: str
    department: str
    dueDate: datetime

class CorrectiveActionCreate(CorrectiveActionBase):
    report_id: int

class CorrectiveAction(CorrectiveActionBase):
    id: int
    report_id: int
    status: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class AIAnalysisBase(BaseModel):
    sifDetected: bool
    confidence: float
    riskScore: int
    riskLevel: str
    hazardCategories: List[str]
    detectedEntities: Dict[str, str]
    potentialConsequences: List[str]
    missingControls: List[str]
    recommendations: List[Dict[str, str]]

class AIAnalysis(AIAnalysisBase):
    id: int
    report_id: int
    modelVersion: str
    analyzedAt: datetime

    class Config:
        from_attributes = True

class SafetyReportBase(BaseModel):
    reportId: str
    reportType: str
    title: str
    description: str
    originalLanguage: Optional[str] = "English"
    site: str
    location: str
    department: str
    activity: str
    reportedBy: str
    severity: str

class SafetyReportCreate(SafetyReportBase):
    pass

class SafetyReport(SafetyReportBase):
    id: int
    detectedLanguage: str
    date: datetime
    status: str
    createdAt: datetime
    updatedAt: datetime
    analysis: Optional[AIAnalysis] = None
    actions: List[CorrectiveAction] = []

    class Config:
        from_attributes = True
