"""
SIF Precursor Classifier for SIFGUARD AI
Identifies Serious Injury & Fatality (SIF) precursors across 12 industrial hazard categories.
Supports multilingual matching across English, Hindi, Marathi, and Gujarati.
"""

from typing import Dict, Any, List, Tuple
import re

HAZARD_TAXONOMY = {
    "Working at Height": {
        "en": ["height", "harness", "scaffold", "scaffolding", "ladder", "fall protection", "elevated", "fall from", "toe board", "edge protection", "lanyard", "safety belt"],
        "hi": ["ऊंचाई", "सेफ्टी बेल्ट", "हार्नेस", "मचान", "सीढ़ी", "गिरने", "ऊंचे स्थान", "सुरक्षा बेल्ट"],
        "mr": ["उंचीवर", "सुरक्षा पट्टा", "पट्टा न वापरता", "शिडी", "पडणे", "उंचावरून", "पडण्याची शक्यता", "मचान"],
        "gu": ["ઊંચાઈ", "સલામતી પટ્ટો", "પટ્ટા વિના", "પડવાની", "સીડી", "હાર્નેસ", "ઊંચી જગ્યાએ"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["Fall from height", "Multiple fractures", "Traumatic brain injury", "Fatality"],
        "missing_controls": ["Fall arrest system / safety harness", "Adequate edge protection / toe boards", "Inspected and tagged scaffolding"],
        "recommended_actions": {
            "immediate": "Stop all elevated work immediately until 100% tie-off fall protection is verified.",
            "control": "Implement mandatory full-body harness with double lanyards and inspected anchorage points.",
            "verification": "Certified scaffolding inspector must verify toe boards and guard rails before resumption.",
            "followup": "Conduct site-wide working-at-height safety stand-down and toolbox talk."
        }
    },
    "Electrical Isolation": {
        "en": ["energized", "electrical", "isolation", "loto", "lockout", "tagout", "live wire", "switchgear", "substation", "breaker", "arc flash", "electrocution", "high voltage", "distribution board", "panel"],
        "hi": ["बिजली", "विद्युत", "ऊर्जावान", "चालू लाइन", "आइसोलेशन", "लॉकाउट", "पैनल", "तार", "शॉक", "स्विचगियर", "हाई वोल्टेज"],
        "mr": ["विजेच्या", "विद्युत", "पॅनेलवर", "पॉवर सप्लाय", "आयसोलेशन", "विद्युत शॉक", "चालू वीज", "वायरिंग"],
        "gu": ["વીજળી", "ઇલેક્ટ્રિકલ", "લાઇવ વાયર", "આઇસોલેશન", "પેનલ", "વીજ પ્રવાહ", "શોક"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["Severe electrocution", "Arc flash burn injury", "Cardiac arrest", "Fatality"],
        "missing_controls": ["Lockout/Tagout (LOTO) physical isolation", "Zero-energy state electrical verification", "Appropriate Arc Flash rated PPE"],
        "recommended_actions": {
            "immediate": "Cease work on panel immediately. Evacuate technicians to safe perimeter.",
            "control": "Implement formal Lockout/Tagout (LOTO) procedure and physically apply master padlock and tag.",
            "verification": "Competent electrical engineer must test for dead/zero energy with calibrated multimeter.",
            "followup": "Review electrical permit-to-work (PTW) compliance audit across all electrical substations."
        }
    },
    "Confined Space": {
        "en": ["confined space", "atmospheric testing", "oxygen", "toxic gas", "vessel entry", "tank cleaning", "manhole", "asphyxiation", "h2s", "nitrogen purge", "enclosed space"],
        "hi": ["सीमित स्थान", "टैंक", "गैस परीक्षण", "कन्फाइंड स्पेस", "ऑक्सीजन", "जहरीली गैस", "दम घुटना"],
        "mr": ["बंदिस्त जागा", "टाकी", "कन्फाइन्ड स्पेस", "ऑक्सिजन तपासणी", "विषारी वायू", "हवेची कमतरता"],
        "gu": ["કન્ફાઈન્ડ સ્પેસ", "ટાંકી", "વાતાવરણ ચકાસણી", "ઝેરી ગેસ", "ઓક્સિજન"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["Toxic gas inhalation", "Hypoxia / Asphyxiation", "Loss of consciousness", "Fatality"],
        "missing_controls": ["Calibrated multi-gas detector atmospheric test", "Confined space entry permit & standby attendant", "Continuous mechanical ventilation & emergency tripod winch"],
        "recommended_actions": {
            "immediate": "Evacuate personnel from confined space immediately until continuous forced-air ventilation is established.",
            "control": "Conduct 4-gas atmospheric testing (O2, LEL, CO, H2S) at top, middle, and bottom levels.",
            "verification": "Designate trained standby attendant at manway with radio communication log.",
            "followup": "Recertify all confined space entry entrants and attendants on rescue protocols."
        }
    },
    "Fire/Explosion": {
        "en": ["fire", "explosion", "gas leak", "hydrocarbon", "flammable", "welding near", "hot work", "spark", "flash fire", "combustible", "flare", "ignition source"],
        "hi": ["आग", "विस्फोट", "गैस रिसाव", "वेल्डिंग", "ज्वलनशील", "धमाका", "चिंगारी", "हॉट वर्क"],
        "mr": ["आग", "स्फोट", "गॅस गळती", "वेल्डिंग", "ज्वलनशील", "ठिणगी", "धुराळा"],
        "gu": ["ગેસ લિકેજ", "આગ", "વેલ્ડિંગ", "વિસ્ફોટ", "હાઇડ્રોકાર્બન", "જ્વલનશીલ"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["Hydrocarbon vapor cloud ignition", "Blast overpressure trauma", "3rd degree thermal burns", "Multiple fatalities"],
        "missing_controls": ["Hot work permit with continuous combustible gas monitoring (LEL < 1%)", "Fire blanket containment and pressurized fire watch extinguisher", "Depressurization and positive hydrocarbon isolation"],
        "recommended_actions": {
            "immediate": "Halt hot work immediately. Isolate gas fuel supply lines and activate area gas monitoring.",
            "control": "Deploy explosion-proof barriers and establish 15m spark containment perimeter.",
            "verification": "Conduct continuous multi-point LEL monitoring; certify 0% combustible gases before resuming.",
            "followup": "Audit Hot Work permitting protocols and inspect all portable fire suppression apparatus."
        }
    },
    "Suspended Load": {
        "en": ["suspended load", "crane", "rigging", "sling", "lifting", "overhead load", "hoist", "drop hazard", "under load", "tag line", "wire rope"],
        "hi": ["क्रेन", "झूलता भार", "सस्पेंडेड लोड", "उठाना", "क्रेन के नीचे", "वायर रोप", "लिफ्टिंग"],
        "mr": ["क्रेन", "लटकणारा भार", "उचलणे", "क्रेन खाली", "वायर रोप", "लिफ्टिंग बेल्ट"],
        "gu": ["ક્રેન", "લટકતો ભાર", "લિફ્ટિંગ", "વાયર દોરડું", "ક્રેનની નીચે"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["Crush injury by falling load", "Catastrophic structural impact", "Fatal blunt force trauma"],
        "missing_controls": ["Exclusion drop-zone barricading", "Tag-line directional control", "Certified lifting gear and rigging load calculation"],
        "recommended_actions": {
            "immediate": "Sound horn and clear all personnel from swing radius and load path immediately.",
            "control": "Erect rigid barricades establishing drop-zone perimeter equal to 1.5x load height.",
            "verification": "Rigger-in-charge must verify third-party certification of web slings and crane load chart.",
            "followup": "Conduct mandatory pre-lift toolbox briefing on Line-of-Fire awareness."
        }
    },
    "Vehicle Interaction": {
        "en": ["vehicle", "forklift", "pedestrian", "collision", "blind spot", "speeding", "traffic", "truck", "loader", "hit by vehicle", "reversing"],
        "hi": ["फोर्कलिफ्ट", "वाहन", "पैदल", "टक्कर", "तेज गति", "ट्रक", "गाड़ी"],
        "mr": ["फोर्कलिफ्ट", "गाडी", "वाहतूक", "वेगाने वाहन चालवणे", "ट्रक", "धडक"],
        "gu": ["ફોર્કલિફ્ટ", "વાહન", "ટ્રક", "ટ્રાફિક", "ઝડપ", "અકસ્માત"],
        "sif_potential": True,
        "default_severity": "High",
        "consequences": ["Pedestrian impact fracture", "Severe crush injury", "Vehicle overturn / fatality"],
        "missing_controls": ["Physical pedestrian walkway segregation", "High-visibility reversing cameras & audible alarms", "Speed limit enforcing barriers"],
        "recommended_actions": {
            "immediate": "Halt vehicle operations until pedestrian segregation barricades are restored.",
            "control": "Install physical bollards segregating pedestrian pathways from heavy equipment transit lanes.",
            "verification": "Inspect functional operability of reverse warning beepers and rotating amber beacons.",
            "followup": "Mandate defensive driving refresher certification for all heavy equipment operators."
        }
    },
    "Pressure Release": {
        "en": ["pressure", "burst", "blowout", "wellhead", "line pressure", "relief valve", "whip check", "flange leak", "pressurized", "hydrotest", "piping rupture"],
        "hi": ["दबाव", "प्रेशर", "ब्लोआउट", "पाइप फटना", "रिलीफ वाल्व", "उच्च दबाव"],
        "mr": ["उच्च दाब", "प्रेशर पाइप", "दाब गळती", "ब्लोआउट", "व्हॉल्व्ह"],
        "gu": ["ઉચ્ચ દબાણ", "પ્રેશર લાઇન", "બ્લોઆઉટ", "વાલ્વ"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["High velocity projectile impact", "Pipeline rupture blast", "Severe trauma or fatality"],
        "missing_controls": ["Whip checks on all pressurized hose connections", "Controlled depressurization & bleed-off verification", "Calibrated pressure safety relief valve"],
        "recommended_actions": {
            "immediate": "Depressurize line to zero bar through designated flare/bleed manifold.",
            "control": "Install certified hose whip-checks and safety clamps on all temporary connections.",
            "verification": "Inspect hydrotest calibration certificate and pressure gauge certification stamp.",
            "followup": "Review line isolation and bleed-down procedural checklist with maintenance supervisors."
        }
    },
    "Chemical Exposure": {
        "en": ["chemical", "acid", "toxic", "h2s", "corrosive", "splash", "fumes", "caustic", "spill", "poison", "msds", "inhalation"],
        "hi": ["रासायनिक", "एसिड", "जहरीला", "गैस रिसाव", "केमिकल", "जलन", "धुआं"],
        "mr": ["रासायनिक", "विषारी", "केमिकल गळती", "ऍसिड", "वायू"],
        "gu": ["રાસાયણિક", "ઝેરી", "એસિડ", "કેમિકલ લિકેજ"],
        "sif_potential": True,
        "default_severity": "High",
        "consequences": ["Chemical pulmonary burns", "Acute toxic poisoning", "Permanent visual impairment"],
        "missing_controls": ["Chemical splash goggles and chemical suit", "Emergency eyewash and safety shower within 10 seconds", "Continuous toxic gas fixed detection sensor"],
        "recommended_actions": {
            "immediate": "Provide immediate emergency wash station access and isolate source valve.",
            "control": "Mandate Level B chemical suit, splash apron, and full-face respirator.",
            "verification": "Test flow rate and temperature of emergency drench showers.",
            "followup": "Review SDS (Safety Data Sheet) handling precautions with all field operatives."
        }
    },
    "Caught-In/Between": {
        "en": ["caught in", "pinch point", "entanglement", "rotating equipment", "roller", "conveyor", "crush", "in running nip", "shaft"],
        "hi": ["फंसना", "पिंच पॉइंट", "घूमने वाला उपकरण", "कन्वेयर", "मशीन में फंसना"],
        "mr": ["अडकणे", "फिरणारे यंत्र", "पिंच पॉइंट", "कन्व्हेअर"],
        "gu": ["ફસાવું", "ફરતા મશીન", "પિંચ પોઈન્ટ"],
        "sif_potential": True,
        "default_severity": "Critical",
        "consequences": ["Limb amputation", "Extensive crush trauma", "Traumatic asphyxiation"],
        "missing_controls": ["Interlocked machine guarding", "Zero-speed mechanical interlock switch", "Emergency pull-cord stop wires"],
        "recommended_actions": {
            "immediate": "Lock out motor drive and apply physical lock on disconnect switch.",
            "control": "Fabricate and install fixed yellow safety interlocked guards over rotating pulleys.",
            "verification": "Verify motor trip within 0.5s when safety trip wire is engaged.",
            "followup": "Conduct machine safeguarding gap analysis across all rotating equipment."
        }
    },
    "Line of Fire": {
        "en": ["line of fire", "stored energy", "spring loaded", "flying debris", "trajectory", "pressurized release", "projectile"],
        "hi": ["लाइन ऑफ फायर", "उड़ता हुआ मलबा", "स्टोर्ड एनर्जी"],
        "mr": ["धोक्याच्या मार्गात", "उडू शकणारे तुकडे"],
        "gu": ["જોખમી ક્ષેત્ર", "લાઇન ઓફ ફાયર"],
        "sif_potential": True,
        "default_severity": "High",
        "consequences": ["Penetrating projectile trauma", "Severe eye trauma", "Blunt force impact"],
        "missing_controls": ["Deflector shields / ballistic containment", "Positioning away from release trajectory", "De-energization of stored mechanical potential"],
        "recommended_actions": {
            "immediate": "Instruct personnel to step outside calculated trajectory zone.",
            "control": "Install energy dampening blast screens and Kevlar wrap around high-stress joints.",
            "verification": "Ensure release path is clear and unpopulated before test cycling.",
            "followup": "Reinforce Line of Fire awareness in daily pre-shift meetings."
        }
    },
    "Machine Safety": {
        "en": ["guard", "machine guard", "nip point", "exposed blades", "saw", "grinder without guard", "unprotected equipment"],
        "hi": ["मशीन गार्ड", "खुला ब्लेड", "ग्राइंडर गार्ड", "बिना सुरक्षा कवर"],
        "mr": ["यंत्र गार्ड", "सुरक्षा कव्हर", "ग्राइंडर"],
        "gu": ["મશીન ગાર્ડ", "કવર વગરનું"],
        "sif_potential": False,
        "default_severity": "Medium",
        "consequences": ["Laceration", "Deep abrasion", "Finger amputation"],
        "missing_controls": ["Compliant wheel guard and eye shield", "Dead-man safety switch"],
        "recommended_actions": {
            "immediate": "Tag equipment Out of Service until approved guard is fitted.",
            "control": "Fit manufacturer original equipment guard and test dead-man switch.",
            "verification": "Toolbox supervisor must inspect guard clearance (max 3mm).",
            "followup": "Audit all portable hand power tools across workshops."
        }
    },
    "PPE Violation": {
        "en": ["ppe", "helmet", "safety glasses", "gloves", "ear plugs", "boots", "coverall", "no goggles"],
        "hi": ["पीपीई", "हेल्मेट", "चश्मा", "दस्ताने", "सुरक्षा जूते"],
        "mr": ["पीपीई", "हेल्मेट", "सुरक्षा चष्मा", "हातमोजे", "सुरक्षा बूट"],
        "gu": ["પીપીઈ", "હેલ્મેટ", "ચશ્મા", "ગ્લોવ્ઝ", "સલામતી બૂટ"],
        "sif_potential": False,
        "default_severity": "Low",
        "consequences": ["Minor eye foreign body", "Hand abrasion", "Superficial laceration"],
        "missing_controls": ["Mandatory PPE compliance enforcement", "Appropriate task-specific PPE availability"],
        "recommended_actions": {
            "immediate": "Provide compliant PPE immediately before allowing work to continue.",
            "control": "Inspect PPE inventory in field storage lockbox.",
            "verification": "Supervisor must record PPE pre-task check on permit sheet.",
            "followup": "Issue positive recognition stickers for workers adhering to safety gear protocols."
        }
    }
}

def classify_sif_and_hazards(text: str, lang_code: str = "en") -> Dict[str, Any]:
    """
    Analyzes safety report text, returns detected hazards, SIF potential, confidence,
    and matching phrase signals.
    """
    text_lower = text.lower()
    matched_hazards = []
    matched_signals = []
    has_sif = False
    max_severity = "Low"
    highest_weight = 0

    severity_weight = {"Low": 1, "Medium": 2, "High": 3, "Critical": 4}

    for hazard_name, spec in HAZARD_TAXONOMY.items():
        # Check all keywords in English + current language + Hindi/Marathi/Gujarati keywords
        keywords = spec["en"] + spec.get(lang_code, []) + spec.get("hi", []) + spec.get("mr", []) + spec.get("gu", [])
        hazard_signals = []
        
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw.lower()) + r'\b', text_lower, re.UNICODE) or (len(kw) > 3 and kw.lower() in text_lower):
                hazard_signals.append(kw)

        if hazard_signals:
            matched_hazards.append({
                "hazard": hazard_name,
                "signals": list(set(hazard_signals)),
                "sif_potential": spec["sif_potential"],
                "severity": spec["default_severity"],
                "missing_controls": spec["missing_controls"],
                "consequences": spec["consequences"],
                "recommended_actions": spec["recommended_actions"]
            })
            matched_signals.extend(hazard_signals)
            
            if spec["sif_potential"]:
                has_sif = True
                
            cur_weight = severity_weight.get(spec["default_severity"], 1)
            if cur_weight > highest_weight:
                highest_weight = cur_weight
                max_severity = spec["default_severity"]

    # Fallback if no specific hazard matched but high-risk words detected
    if not matched_hazards:
        generic_sif_words = ["die", "fatal", "kill", "hospital", "amputat", "serious", "मृत्यू", "गंभीर", "मरण", "इजा", "मौत"]
        for g in generic_sif_words:
            if g in text_lower:
                has_sif = True
                max_severity = "High"
                matched_signals.append(g)
                matched_hazards.append({
                    "hazard": "General Unsafe Condition",
                    "signals": [g],
                    "sif_potential": True,
                    "severity": "High",
                    "missing_controls": ["Comprehensive site risk assessment", "Permit to Work compliance"],
                    "consequences": ["Serious workplace injury"],
                    "recommended_actions": HAZARD_TAXONOMY["Machine Safety"]["recommended_actions"]
                })
                break

    if not matched_hazards:
        matched_hazards.append({
            "hazard": "General Safety Observation",
            "signals": [],
            "sif_potential": False,
            "severity": "Low",
            "missing_controls": ["Routine supervision and housekeeping"],
            "consequences": ["Minor disruption"],
            "recommended_actions": HAZARD_TAXONOMY["PPE Violation"]["recommended_actions"]
        })

    # Confidence calculation based on number and specificity of signal triggers
    signal_count = len(set(matched_signals))
    confidence = min(0.98, max(0.82, 0.85 + (signal_count * 0.03)))
    
    return {
        "sif_detected": has_sif,
        "max_severity": max_severity,
        "hazard_categories": [h["hazard"] for h in matched_hazards],
        "matched_details": matched_hazards,
        "signals": list(set(matched_signals)),
        "confidence": round(confidence, 2)
    }
