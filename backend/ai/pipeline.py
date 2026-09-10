"""
Unified Safety Intelligence AI Pipeline for SIFGUARD AI
Orchestrates:
Language Detection -> Entity Extraction -> SIF Precursor Classification ->
Risk Scoring -> Explainability & Consequence Chain -> AI Recommendations
"""

from typing import Dict, Any, List
from .language_detector import detect_language
from .sif_classifier import classify_sif_and_hazards
from .entity_extractor import extract_safety_entities
from .risk_scorer import calculate_risk_score
from .explainability import generate_explanation_and_chain

MODEL_METADATA = {
    "name": "SIFGUARD Industrial NLP Engine",
    "version": "v2.4-hybrid-indic",
    "type": "Modular Safety NLP & Deterministic Ontology Rule Engine",
    "disclaimer": "Demo Industrial NLP Engine: Configurable model for SIH demonstration. Provides decision support and does not replace certified safety officer judgment."
}

def analyze_safety_report(
    description: str,
    selected_language: str = "auto",
    all_historical_reports: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Executes the full 7-step safety intelligence analysis pipeline.
    """
    # Step 1 & 2: Language Detection
    if selected_language and selected_language != "auto":
        lang_info = {
            "code": selected_language,
            "name": {"en": "English", "hi": "Hindi", "mr": "Marathi", "gu": "Gujarati"}.get(selected_language, "English"),
            "confidence": 0.99,
            "detected_script": "Specified"
        }
    else:
        lang_info = detect_language(description)

    # Step 3: SIF and Hazard Classification (multilingual aware)
    classification = classify_sif_and_hazards(description, lang_info["code"])
    has_sif = classification["sif_detected"]
    hazard_categories = classification["hazard_categories"]
    max_severity = classification["max_severity"]
    signals = classification["signals"]
    ai_confidence = classification["confidence"]

    # Step 4: Safety Entity Extraction
    entities = extract_safety_entities(description, hazard_categories)

    # Step 5: Risk Assessment & Scoring
    risk_data = calculate_risk_score(has_sif, max_severity, hazard_categories, description)

    # Step 6: Explainability & Consequence Chain
    explainability = generate_explanation_and_chain(
        description, hazard_categories, entities, signals, has_sif
    )

    # Step 7: Structured Recommendations
    primary_hazard_detail = classification["matched_details"][0] if classification["matched_details"] else {}
    recommended_actions = primary_hazard_detail.get("recommended_actions", {
        "immediate": "Cease affected work operations until safety supervisor conducts risk assessment.",
        "control": "Implement standard engineered barrier and verify Permit to Work controls.",
        "verification": "Supervisor on-duty must visually inspect and sign off control checklist.",
        "followup": "Review finding in next shift changeover safety briefing."
    })

    potential_consequences = primary_hazard_detail.get("consequences", [
        "Uncontrolled energy release", "Lost time injury", "Potential Serious Injury or Fatality"
    ])

    return {
        "sif_detected": has_sif,
        "risk_level": risk_data["risk_level"],
        "risk_score": risk_data["risk_score"],
        "level_color": risk_data["level_color"],
        "confidence": int(ai_confidence * 100),
        "confidence_disclaimer": "AI confidence represents the model's estimated certainty for this classification. It is intended to support, not replace, qualified safety judgment.",
        "language_info": lang_info,
        "hazard_categories": hazard_categories,
        "primary_hazard": hazard_categories[0] if hazard_categories else "Unsafe Condition",
        "detected_entities": entities,
        "risk_factors": risk_data["factors"],
        "risk_disclaimer": risk_data["framework_disclaimer"],
        "potential_consequences": potential_consequences,
        "missing_controls": entities.get("missing_controls", []),
        "recommendations": recommended_actions,
        "explainability": explainability,
        "model_metadata": MODEL_METADATA
    }
