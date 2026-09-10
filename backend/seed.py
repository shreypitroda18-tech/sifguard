import datetime
from sqlalchemy.orm import Session
import database, models, schemas, ai_engine

models.Base.metadata.create_all(bind=database.engine)

def seed_data():
    db = database.SessionLocal()
    
    # Check if we already have data
    if db.query(models.SafetyReport).count() > 0:
        print("Database already seeded")
        db.close()
        return

    # Create dummy reports
    reports = [
        models.SafetyReport(
            reportId="OIL-1001",
            reportType="Unsafe Act",
            title="Technician working without isolation",
            description="During maintenance, the technician was working on energized electrical equipment without proper isolation.",
            site="Site A",
            location="Maintenance Bay 2",
            department="Electrical",
            activity="Maintenance",
            reportedBy="John Doe",
            severity="High"
        ),
        models.SafetyReport(
            reportId="OIL-1002",
            reportType="Unsafe Condition",
            title="Missing fall protection",
            description="Worker observed at elevated platform without appropriate fall protection.",
            site="Site B",
            location="Tower 4",
            department="Operations",
            activity="Inspection",
            reportedBy="Jane Smith",
            severity="Critical"
        ),
        models.SafetyReport(
            reportId="OIL-1003",
            reportType="Unsafe Act",
            title="Marathi Report - Working at height",
            description="कामगार सुरक्षा पट्टा न वापरता उंचीवर काम करत होता.",
            site="Site A",
            location="Platform 1",
            department="Operations",
            activity="Cleaning",
            reportedBy="Ramesh M.",
            severity="High",
            originalLanguage="Marathi"
        ),
        models.SafetyReport(
            reportId="OIL-1004",
            reportType="Near Miss",
            title="Forklift near pedestrian",
            description="Forklift operating in pedestrian movement zone without spotter.",
            site="Site C",
            location="Warehouse",
            department="Logistics",
            activity="Transport",
            reportedBy="Mike T.",
            severity="Medium"
        ),
    ]
    
    for report in reports:
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # Run AI analysis
        analysis_result = ai_engine.analyze_safety_report(report.description, report.originalLanguage)
        report.detectedLanguage = analysis_result.pop("detectedLanguage")
        db_analysis = models.AIAnalysis(**analysis_result, report_id=report.id)
        db.add(db_analysis)
        
        # Create an action for some
        if report.severity in ["High", "Critical"]:
            action = models.CorrectiveAction(
                report_id=report.id,
                title=f"Fix {report.title}",
                description=f"Address issue: {report.description}",
                priority=report.severity,
                assignedTo="Supervisor",
                department=report.department,
                dueDate=datetime.datetime.utcnow() + datetime.timedelta(days=7)
            )
            db.add(action)
            
        db.commit()

    print("Database seeded with demo data")
    db.close()

if __name__ == "__main__":
    seed_data()
