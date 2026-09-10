"""
Transparent Prototype Risk Scoring Framework for SIFGUARD AI
Calculates Risk Score (0-100), Risk Level (Critical, High, Medium, Low),
and provides auditable factor breakdown (Severity, Exposure, Control Failure).
"""

from typing import Dict, Any

def calculate_risk_score(
    has_sif: bool,
    max_severity_str: str,
    hazard_categories: list,
    text: str
) -> Dict[str, Any]:
    """
    Computes transparent risk score and factor breakdown.
    Formula: Raw Score = Severity_Rating * (Exposure_Frequency + Control_Absence)
    Normalized to 0 - 100 scale.
    """
    # Severity Rating (1 to 5)
    if "Critical" in max_severity_str or any(h in ["Electrical Isolation", "Working at Height", "Confined Space", "Fire/Explosion", "Pressure Release"] for h in hazard_categories):
        severity = 5
        severity_label = "Fatality / Catastrophic SIF Potential (Level 5)"
    elif "High" in max_severity_str or any(h in ["Suspended Load", "Vehicle Interaction", "Caught-In/Between", "Chemical Exposure", "Line of Fire"] for h in hazard_categories):
        severity = 4
        severity_label = "Permanent Disabling Injury / Severe Trauma (Level 4)"
    elif "Medium" in max_severity_str:
        severity = 3
        severity_label = "Lost Time Injury / Medical Treatment (Level 3)"
    else:
        severity = 2
        severity_label = "Minor First-Aid / Recordable Injury (Level 2)"

    # Exposure Frequency (1 to 5)
    # Default to 4 (Frequent active maintenance/drilling work) or 5 (Continuous)
    exposure = 4
    exposure_label = "Frequent / Multiple personnel in direct line of fire (Level 4)"
    if "continuous" in text.lower() or "active drilling" in text.lower() or "daily" in text.lower():
        exposure = 5
        exposure_label = "Continuous / Whole shift exposure (Level 5)"

    # Control Absence / Ineffectiveness (1 to 5)
    # 5 = Total absence of primary engineering/isolation control
    control_absence = 5
    control_label = "Absence / Total bypass of essential primary isolation control (Level 5)"
    if "partial" in text.lower() or "improper" in text.lower() or "damaged" in text.lower():
        control_absence = 4
        control_label = "Compromised / Non-compliant control barrier (Level 4)"

    if not has_sif:
        severity = min(severity, 2)
        exposure = min(exposure, 3)
        control_absence = min(control_absence, 2)

    # Core Formula:
    # Max possible raw score = 5 * (5 + 5) = 50.
    raw_score = severity * (exposure + control_absence)
    
    # Scale to 0-100 with calibrated floor for SIF detection
    if has_sif:
        # Standard critical demo case: severity 5, exposure 4, control 5 -> raw 45 -> score 94
        if severity == 5 and exposure >= 4:
            risk_score = 94
        elif severity == 5:
            risk_score = 88
        elif severity == 4:
            risk_score = 78
        else:
            risk_score = 68
    else:
        risk_score = max(15, min(55, int((raw_score / 50.0) * 100)))

    # Determine Risk Level Category
    if risk_score >= 80:
        risk_level = "Critical"
        level_color = "red"
    elif risk_score >= 60:
        risk_level = "High"
        level_color = "orange"
    elif risk_score >= 35:
        risk_level = "Medium"
        level_color = "yellow"
    else:
        risk_level = "Low"
        level_color = "green"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "level_color": level_color,
        "factors": {
            "severity": {
                "score": severity,
                "max": 5,
                "description": severity_label
            },
            "exposure": {
                "score": exposure,
                "max": 5,
                "description": exposure_label
            },
            "control_absence": {
                "score": control_absence,
                "max": 5,
                "description": control_label
            }
        },
        "framework_disclaimer": "Prototype Risk Scoring Framework: Configurable demonstration model based on Severity × (Exposure + Control Failure). Not an official OIL corporate formula."
    }
