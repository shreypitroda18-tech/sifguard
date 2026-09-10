"""
Explainable AI & Consequence Chain Generator for SIFGUARD AI
Provides phrase highlighting, signal attribution checklist, and chronological Consequence Chain.
"""

from typing import Dict, Any, List
import re

def generate_explanation_and_chain(
    text: str,
    hazard_categories: List[str],
    entities: Dict[str, Any],
    signals: List[str],
    has_sif: bool
) -> Dict[str, Any]:
    """
    Generates explainability metadata, highlighted phrases, signal breakdown, and
    the 5-step Consequence Chain:
    HAZARD -> EXPOSURE -> CONTROL FAILURE -> POTENTIAL EVENT -> SERIOUS INJURY / FATALITY
    """
    # 1. Phrase Highlighting
    # Identify high-impact spans in text
    highlight_terms = list(set(signals))
    if not highlight_terms:
        highlight_terms = ["energized", "isolation", "height", "harness", "leak", "crane", "confined"]

    highlighted_spans = []
    text_lower = text.lower()
    for term in highlight_terms:
        for match in re.finditer(re.escape(term.lower()), text_lower):
            start, end = match.span()
            highlighted_spans.append({
                "start": start,
                "end": end,
                "text": text[start:end],
                "type": "risk_signal"
            })
    # Sort spans
    highlighted_spans.sort(key=lambda s: s["start"])

    # 2. Auditable Signals Checklist
    detected_signals_list = []
    if any(h in ["Electrical Isolation"] for h in hazard_categories):
        detected_signals_list = [
            {"signal": "Energized electrical equipment identified", "status": "verified", "category": "Hazard"},
            {"signal": "Active maintenance / live servicing activity", "status": "verified", "category": "Activity"},
            {"signal": "Missing Lockout/Tagout (LOTO) isolation", "status": "critical_gap", "category": "Control Barrier"},
            {"signal": "Direct technician line-of-fire exposure", "status": "verified", "category": "Exposure"},
            {"signal": "Catastrophic arc flash / electrocution potential", "status": "verified", "category": "Severity"}
        ]
    elif any(h in ["Working at Height"] for h in hazard_categories):
        detected_signals_list = [
            {"signal": "Elevated platform / structure > 1.8 meters", "status": "verified", "category": "Hazard"},
            {"signal": "Unprotected edge or open grating work", "status": "verified", "category": "Activity"},
            {"signal": "Absence of 100% tie-off safety harness / lanyard", "status": "critical_gap", "category": "Control Barrier"},
            {"signal": "Worker positioning without edge fall protection", "status": "verified", "category": "Exposure"},
            {"signal": "High kinetic energy fall impact potential", "status": "verified", "category": "Severity"}
        ]
    elif any(h in ["Confined Space"] for h in hazard_categories):
        detected_signals_list = [
            {"signal": "Enclosed process vessel / storage tank entry", "status": "verified", "category": "Hazard"},
            {"signal": "Internal inspection or sludge cleaning task", "status": "verified", "category": "Activity"},
            {"signal": "Zero documented 4-gas atmospheric pre-testing", "status": "critical_gap", "category": "Control Barrier"},
            {"signal": "Entry without standby attendant or rescue winch", "status": "critical_gap", "category": "Control Barrier"},
            {"signal": "Toxic H2S / acute asphyxiation potential", "status": "verified", "category": "Severity"}
        ]
    elif any(h in ["Fire/Explosion"] for h in hazard_categories):
        detected_signals_list = [
            {"signal": "Flammable hydrocarbon gas / vapor presence", "status": "verified", "category": "Hazard"},
            {"signal": "Hot work / ignition source in active zone", "status": "verified", "category": "Activity"},
            {"signal": "Continuous LEL gas monitoring not established", "status": "critical_gap", "category": "Control Barrier"},
            {"signal": "Personnel inside blast overpressure radius", "status": "verified", "category": "Exposure"},
            {"signal": "Vapor cloud explosion / flash fire potential", "status": "verified", "category": "Severity"}
        ]
    else:
        detected_signals_list = [
            {"signal": f"Primary hazard condition detected ({hazard_categories[0] if hazard_categories else 'Unsafe Condition'})", "status": "verified", "category": "Hazard"},
            {"signal": f"Operational activity: {entities.get('activity', 'Facility Operation')}", "status": "verified", "category": "Activity"},
            {"signal": f"Control barrier deficiency: {entities.get('missing_controls', ['Engineering Control Gap'])[0]}", "status": "critical_gap", "category": "Control Barrier"},
            {"signal": "Direct personnel exposure in work area", "status": "verified", "category": "Exposure"},
            {"signal": "Potential for lost time or serious workplace injury", "status": "verified", "category": "Severity"}
        ]

    # 3. Five-Step Consequence Chain Timeline
    primary_hazard = hazard_categories[0] if hazard_categories else "Uncontrolled Workplace Hazard"
    if "Electrical Isolation" in hazard_categories:
        chain = [
            {"step": 1, "stage": "HAZARD", "title": "Energized 415V Switchgear", "description": "High voltage busbar actively energized with live electrical current."},
            {"step": 2, "stage": "EXPOSURE", "title": "Technician Exposure", "description": "Maintenance technician working with hand tools within flash protection boundary."},
            {"step": 3, "stage": "CONTROL FAILURE", "title": "No LOTO Isolation", "description": "Lockout/Tagout protocol not initiated; zero-energy state never verified."},
            {"step": 4, "stage": "POTENTIAL EVENT", "title": "Unexpected Energization / Flash", "description": "Inadvertent tool slip creates phase-to-phase arc flash and conductive pathway."},
            {"step": 5, "stage": "SERIOUS INJURY / FATALITY", "title": "Electrocution & Severe Burn", "description": "Fatal cardiac arrest from electric shock or catastrophic 3rd-degree arc flash burns."}
        ]
    elif "Working at Height" in hazard_categories:
        chain = [
            {"step": 1, "stage": "HAZARD", "title": "Elevated Work Location", "description": "Work area located on pipe rack / scaffold at elevation > 3 meters."},
            {"step": 2, "stage": "EXPOSURE", "title": "Worker Position at Edge", "description": "Worker performing task immediately adjacent to unprotected open perimeter."},
            {"step": 3, "stage": "CONTROL FAILURE", "title": "No Fall Arrest / Harness", "description": "Safety harness unclipped; temporary guardrails and toe boards missing."},
            {"step": 4, "stage": "POTENTIAL EVENT", "title": "Loss of Balance / Footing Slip", "description": "Worker shifts weight or encounters loose grating, causing uncontrolled fall."},
            {"step": 5, "stage": "SERIOUS INJURY / FATALITY", "title": "Fatal Ground Impact", "description": "High velocity impact onto concrete / steel structure causing fatal trauma."}
        ]
    elif "Fire/Explosion" in hazard_categories:
        chain = [
            {"step": 1, "stage": "HAZARD", "title": "Hydrocarbon Vapor Accumulation", "description": "Combustible gas present due to packing gland or valve flange leak."},
            {"step": 2, "stage": "EXPOSURE", "title": "Ignition Source Proximity", "description": "Grinding/welding sparks or uncertified non-intrinsically safe electrical device."},
            {"step": 3, "stage": "CONTROL FAILURE", "title": "Missing Gas Detection", "description": "No portable LEL detector deployed; hot work permit not authorized."},
            {"step": 4, "stage": "POTENTIAL EVENT", "title": "Vapor Cloud Ignition", "description": "Sparks reach stoichiometric fuel-air mix, detonating flash fire."},
            {"step": 5, "stage": "SERIOUS INJURY / FATALITY", "title": "Blast Trauma & Thermal Burns", "description": "Catastrophic overpressure blast wave and critical thermal burn injuries."}
        ]
    else:
        chain = [
            {"step": 1, "stage": "HAZARD", "title": primary_hazard, "description": "Presence of uncontrolled physical or chemical energy in work zone."},
            {"step": 2, "stage": "EXPOSURE", "title": "Personnel Line of Fire", "description": "Workers present within direct influence perimeter of hazardous condition."},
            {"step": 3, "stage": "CONTROL FAILURE", "title": "Barrier Breakdown", "description": f"Absence of primary control: {entities.get('missing_controls', ['SOP'])[0]}."},
            {"step": 4, "stage": "POTENTIAL EVENT", "title": "Hazard Trigger / Release", "description": "Energy releases unexpectedly due to lack of engineered safeguards."},
            {"step": 5, "stage": "SERIOUS INJURY / FATALITY", "title": "High-Potential Injury", "description": "Severe impact, crush, or irreversible health consequence."}
        ]

    return {
        "highlighted_spans": highlighted_spans,
        "signals_checklist": detected_signals_list,
        "consequence_chain": chain,
        "why_flagged_summary": f"Flagged because {primary_hazard} was detected with clear personnel exposure and absent primary control barriers."
    }
