"""
Safety Entity Extractor for SIFGUARD AI
Extracts structured industrial entities from safety observations:
- Activity (e.g., Electrical Maintenance, Hot Work, Tank Inspection)
- Equipment / Asset (e.g., Switchgear, Scaffolding, Pressure Valve)
- Exposed Personnel (e.g., Contract Technician, Welder, Pedestrian)
- Missing Controls (e.g., LOTO Isolation, Safety Harness, Gas Detector)
"""

from typing import Dict, Any, List
import re

ACTIVITY_PATTERNS = [
    (r"(maintenance|repair|overhaul|servicing|दुरुस्ती|मरम्मत|સમારકામ)", "Electrical / Mechanical Maintenance"),
    (r"(welding|cutting|grinding|hot work|वेल्डिंग|हॉट वर्क)", "Hot Work / Welding Operations"),
    (r"(scaffold|height|roof|ladder|उंचीवर|ऊंचाई|ઊંચાઈ)", "Working at Height / Elevated Access"),
    (r"(confined space|tank entry|vessel|टाकी|टैंक|ટાંકી)", "Confined Space Entry & Tank Cleaning"),
    (r"(rigging|crane|lifting|hoisting|क्रेन|लिफ्टिंग)", "Crane Lifting & Rigging Operations"),
    (r"(driving|forklift|truck|transport|वाहन|गाडी)", "Heavy Vehicle & Plant Transit"),
    (r"(pipeline|flange|hydrotest|pipe|पाइपलाइन|પાઇપલાઇન)", "Pressurized Pipeline Operations"),
    (r"(chemical handling|acid wash|chemical|केमिकल|एसिड)", "Hazardous Chemical Handling")
]

EQUIPMENT_PATTERNS = [
    (r"(panel|switchgear|breaker|substation|cable|wire|विजेच्या पॅनेल|पैनल|पेનલ)", "415V/11kV Electrical Switchgear Panel"),
    (r"(scaffold|ladder|platform|मचान|सीढ़ी|शिडी|સીડી)", "Tubular Mobile Scaffolding Platform"),
    (r"(crane|boom|hoist|sling|rope|क्रेन|वायर रोप)", "Heavy Crawler Crane & Synthetic Web Slings"),
    (r"(forklift|loader|truck|vehicle|फोर्कलिफ्ट|ट्रक)", "Industrial Diesel Forklift Unit"),
    (r"(pipeline|valve|flange|manifold|pipe|वाल्व|पाइप|વાલ્વ)", "High-Pressure Hydrocarbon Piping & Manifold"),
    (r"(tank|vessel|drum|column|separator|टाकी|टैंक)", "Crude Oil Storage Vessel / Vessel Internal"),
    (r"(compressor|pump|motor|generator|पंप)", "Reciprocating Gas Compressor / High-Flow Pump")
]

PEOPLE_PATTERNS = [
    (r"(technician|electrician|ऑपरेटर|इलेक्ट्रिशियन)", "Electrical / Instrumentation Technician"),
    (r"(contract worker|contractor|मजदूर|कंत्राटी कामगार|કોન્ટ્રાક્ટ કામદાર)", "Contract Maintenance Operative"),
    (r"(welder|fitter|वेल्डर)", "Certified High-Pressure Pipe Welder"),
    (r"(rigger|crane operator|रिंगर|क्रेन ऑपरेटर)", "Heavy Lift Crane Rigger"),
    (r"(worker|personnel|कामगार|कर्मचारी|કામદાર)", "Site Operational Personnel"),
    (r"(supervisor|engineer|इंजीनियर|पर्यवेक्षक)", "Area Operational Supervisor")
]

def extract_safety_entities(text: str, detected_hazards: List[str] = None) -> Dict[str, Any]:
    """
    Extracts structured entities from the report text.
    """
    detected_activity = "Industrial Facility Operations"
    for pattern, activity_name in ACTIVITY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            detected_activity = activity_name
            break

    detected_equipment = "Industrial Plant Equipment"
    for pattern, equip_name in EQUIPMENT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            detected_equipment = equip_name
            break

    detected_people = "Operations Technician / Worker"
    for pattern, people_name in PEOPLE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            detected_people = people_name
            break

    # Contextual missing controls based on text and hazards
    controls = []
    if any(h in (detected_hazards or []) for h in ["Electrical Isolation"]):
        controls.append("Lockout/Tagout (LOTO) Physical De-energization")
        controls.append("Zero Energy Calibrated Voltage Verification")
    elif any(h in (detected_hazards or []) for h in ["Working at Height"]):
        controls.append("100% Tie-Off Full Body Safety Harness with Double Lanyard")
        controls.append("Inspected Green-Tagged Scaffolding with Toe Boards")
    elif any(h in (detected_hazards or []) for h in ["Confined Space"]):
        controls.append("Continuous 4-Gas Atmospheric Testing (O2, LEL, CO, H2S)")
        controls.append("Dedicated Standby Safety Attendant & Tripod Winch")
    elif any(h in (detected_hazards or []) for h in ["Fire/Explosion"]):
        controls.append("Continuous Combustible Gas Monitoring (< 1% LEL)")
        controls.append("Hot Work Permit with Charged Fire Watch Line")
    elif any(h in (detected_hazards or []) for h in ["Suspended Load"]):
        controls.append("Rigid Exclusion Drop-Zone Barricading")
        controls.append("Dual Tag Lines for Directional Load Guide")
    elif any(h in (detected_hazards or []) for h in ["Vehicle Interaction"]):
        controls.append("Physical Pedestrian Segregation Barriers")
        controls.append("Audible Reversing Alarm & Amber Warning Strobe")
    else:
        controls.append("Standard Operating Procedure (SOP) Compliance")
        controls.append("Task Risk Assessment & Pre-Job Safety Briefing")

    return {
        "activity": detected_activity,
        "equipment": detected_equipment,
        "exposed_personnel": detected_people,
        "missing_controls": controls,
        "immediate_condition": "Work ongoing in direct vicinity of uncontrolled hazard"
    }
