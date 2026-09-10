from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, database, ai_engine
from typing import List

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SIFGUARD AI API", description="Backend for SIFGUARD AI Safety Intelligence Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(database.get_db)):
    reports_count = db.query(models.SafetyReport).count()
    sif_count = db.query(models.AIAnalysis).filter(models.AIAnalysis.sifDetected == True).count()
    critical_count = db.query(models.AIAnalysis).filter(models.AIAnalysis.riskLevel == "Critical").count()
    open_actions = db.query(models.CorrectiveAction).filter(models.CorrectiveAction.status == "Open").count()
    
    return {
        "totalReports": reports_count,
        "sifPrecursors": sif_count,
        "criticalRisks": critical_count,
        "openActions": open_actions
    }

@app.post("/api/reports", response_model=schemas.SafetyReport)
def create_report(report: schemas.SafetyReportCreate, db: Session = Depends(database.get_db)):
    db_report = models.SafetyReport(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/api/reports", response_model=List[schemas.SafetyReport])
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    reports = db.query(models.SafetyReport).offset(skip).limit(limit).all()
    return reports

@app.get("/api/reports/{report_id}", response_model=schemas.SafetyReport)
def get_report(report_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.SafetyReport).filter(models.SafetyReport.id == report_id).first()
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.post("/api/reports/{report_id}/analyze", response_model=schemas.AIAnalysis)
def analyze_report(report_id: int, db: Session = Depends(database.get_db)):
    report = db.query(models.SafetyReport).filter(models.SafetyReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    analysis_result = ai_engine.analyze_safety_report(report.description, report.originalLanguage)
    
    # Update report language if detected
    report.detectedLanguage = analysis_result.pop("detectedLanguage")
    
    # Check if analysis exists
    db_analysis = db.query(models.AIAnalysis).filter(models.AIAnalysis.report_id == report_id).first()
    
    if db_analysis:
        for key, value in analysis_result.items():
            setattr(db_analysis, key, value)
    else:
        db_analysis = models.AIAnalysis(**analysis_result, report_id=report_id)
        db.add(db_analysis)
        
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@app.get("/api/actions", response_model=List[schemas.CorrectiveAction])
def get_actions(db: Session = Depends(database.get_db)):
    return db.query(models.CorrectiveAction).all()

@app.post("/api/actions", response_model=schemas.CorrectiveAction)
def create_action(action: schemas.CorrectiveActionCreate, db: Session = Depends(database.get_db)):
    db_action = models.CorrectiveAction(**action.dict())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@app.patch("/api/actions/{action_id}")
def update_action_status(action_id: int, status: str, db: Session = Depends(database.get_db)):
    action = db.query(models.CorrectiveAction).filter(models.CorrectiveAction.id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    action.status = status
    db.commit()
    return action

@app.post("/api/assistant/query")
def copilot_query(query: str, lang: str = "en", db: Session = Depends(database.get_db)):
    # Very simple mock deterministic QA engine for demo
    q = query.lower()
    if "hazard" in q or "खतरे" in q:
        return {"answer": "The most frequent hazards this month are Working at Height and Electrical Isolation."}
    if "site" in q or "कुठे" in q:
        return {"answer": "Site A currently has the highest concentration of critical observations."}
    return {"answer": "Based on the safety intelligence data, I can see 126 critical reports. Most are related to electrical and height hazards."}
