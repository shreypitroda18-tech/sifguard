import re

def analyze_safety_report(description: str, original_language: str = "English") -> dict:
    # Deterministic NLP engine for demo purposes
    desc_lower = description.lower()
    
    # Simple language detection mock
    detected_lang = original_language
    if re.search(r"[\u0900-\u097F]", description):
        detected_lang = "Hindi / Marathi"
    if re.search(r"[\u0A80-\u0AFF]", description):
        detected_lang = "Gujarati"
        
    # Hazard Dictionary
    hazards = []
    consequences = []
    controls = []
    entities = {}
    
    # Working at Height
    if any(keyword in desc_lower for keyword in ["height", "harness", "elevated", "fall", "उंचीवर", "ऊंचाई"]):
        hazards.append("Working at Height")
        consequences.append("Fall from height leading to Serious Injury/Fatality")
        controls.append("Fall Protection System")
        entities["Hazard"] = "Working at Height"
        
    # Electrical Isolation
    if any(keyword in desc_lower for keyword in ["electrical", "energized", "isolation", "loto", "shock"]):
        hazards.append("Electrical Isolation")
        consequences.append("Electrocution / Arc Flash")
        controls.append("Lockout/Tagout (LOTO)")
        entities["Activity"] = "Electrical Work"
        
    # Confined Space
    if any(keyword in desc_lower for keyword in ["confined space", "ventilation", "atmospheric", "tank"]):
        hazards.append("Confined Space")
        consequences.append("Asphyxiation / Toxic Exposure")
        controls.append("Atmospheric Testing & Ventilation")
        entities["Location"] = "Confined Space"
        
    # Vehicle Interaction
    if any(keyword in desc_lower for keyword in ["vehicle", "forklift", "pedestrian", "collision"]):
        hazards.append("Vehicle Interaction")
        consequences.append("Struck-by / Crushing Injury")
        controls.append("Traffic Management Plan")
        entities["Equipment"] = "Vehicle / Forklift"
        
    # PPE
    if any(keyword in desc_lower for keyword in ["no ppe", "without ppe", "safety belt", "पट्टा", "પટ્ટા"]):
        if "PPE" not in hazards: hazards.append("Lack of PPE")
        controls.append("Appropriate Personal Protective Equipment")
        entities["Missing Control"] = "PPE"

    # Determine SIF and Risk
    sif_detected = len(hazards) > 0
    confidence = 0.85 + (len(hazards) * 0.03)
    if confidence > 0.98: confidence = 0.98
    
    risk_score = 40
    risk_level = "Low"
    
    if sif_detected:
        if any(h in hazards for h in ["Electrical Isolation", "Working at Height", "Confined Space"]):
            risk_score = 90 + (len(hazards) * 2)
            risk_level = "Critical"
        else:
            risk_score = 70 + (len(hazards) * 5)
            risk_level = "High"
            
    if risk_score > 99: risk_score = 99
    
    # Generate Recommendations
    recommendations = []
    if risk_level == "Critical":
        recommendations.append({"priority": "Immediate", "action": "Stop work immediately until appropriate controls are verified."})
    
    for control in controls:
        recommendations.append({"priority": "High", "action": f"Implement {control} before proceeding."})
        
    if not recommendations:
        recommendations.append({"priority": "Medium", "action": "Review general safety protocols."})

    return {
        "detectedLanguage": detected_lang,
        "sifDetected": sif_detected,
        "confidence": round(confidence, 2),
        "riskScore": int(risk_score),
        "riskLevel": risk_level,
        "hazardCategories": hazards,
        "detectedEntities": entities,
        "potentialConsequences": consequences,
        "missingControls": controls,
        "recommendations": recommendations
    }
