"""
Comprehensive Seed Dataset for SIFGUARD AI
Includes 65+ realistic industrial Oil & Gas safety reports (English, Hindi, Marathi, Gujarati),
audit timelines, corrective actions, operational plant zones, and demo users.
"""

from datetime import datetime, timedelta
import random

DEMO_USERS = [
    {
        "id": "usr-1",
        "name": "Rajesh Sharma",
        "email": "safety.officer@oilindia.in",
        "role": "Safety Officer",
        "department": "Corporate HSE & Loss Prevention",
        "site": "All Sites",
        "avatar": "RS",
        "permissions": ["view_all", "analyze_reports", "create_actions", "verify_actions", "view_analytics", "export_data"]
    },
    {
        "id": "usr-2",
        "name": "Anita Desai",
        "email": "admin@oilindia.in",
        "role": "Admin",
        "department": "Safety Systems & IT",
        "site": "Headquarters",
        "avatar": "AD",
        "permissions": ["admin_all", "manage_users", "manage_settings", "view_all", "analyze_reports", "create_actions", "verify_actions"]
    },
    {
        "id": "usr-3",
        "name": "Vikram Singh",
        "email": "supervisor@oilindia.in",
        "role": "Supervisor",
        "department": "Mechanical & Electrical Maintenance",
        "site": "Moran Wellhead A",
        "avatar": "VS",
        "permissions": ["view_assigned", "update_actions", "upload_evidence", "request_verification"]
    },
    {
        "id": "usr-4",
        "name": "Sanjay Patel",
        "email": "manager@oilindia.in",
        "role": "Manager",
        "department": "Plant Operations",
        "site": "Duliajan Plant 2",
        "avatar": "SP",
        "permissions": ["view_all", "view_analytics", "view_risk_intelligence", "export_data"]
    },
    {
        "id": "usr-5",
        "name": "Amit Kumar",
        "email": "employee@oilindia.in",
        "role": "Employee",
        "department": "Field Operations",
        "site": "Digboi Rig 4",
        "avatar": "AK",
        "permissions": ["submit_report", "view_own_reports", "view_assigned_actions"]
    }
]

# Operational Plant Zones for Heatmap
PLANT_ZONES = [
    {
        "id": "zone-drilling",
        "name": "Drilling & Well Operations",
        "risk_score": 84,
        "risk_level": "Critical",
        "report_count": 312,
        "critical_reports": 38,
        "sif_precursors": 64,
        "top_hazards": ["Pressure Release", "Suspended Load", "Working at Height"],
        "lead_supervisor": "H. Borah (Senior Toolpusher)",
        "trend": "+12% vs last month"
    },
    {
        "id": "zone-maintenance",
        "name": "Electrical & Mechanical Maintenance",
        "risk_score": 89,
        "risk_level": "Critical",
        "report_count": 420,
        "critical_reports": 52,
        "sif_precursors": 78,
        "top_hazards": ["Electrical Isolation", "Caught-In/Between", "Line of Fire"],
        "lead_supervisor": "Vikram Singh (Maintenance Supv)",
        "trend": "+28% (LOTO surges)"
    },
    {
        "id": "zone-storage",
        "name": "Crude Storage & Tank Farm",
        "risk_score": 72,
        "risk_level": "High",
        "report_count": 185,
        "critical_reports": 18,
        "sif_precursors": 31,
        "top_hazards": ["Confined Space", "Chemical Exposure", "Working at Height"],
        "lead_supervisor": "P. Gogoi (Terminal Supt)",
        "trend": "-4% vs last month"
    },
    {
        "id": "zone-processing",
        "name": "Hydrocarbon Processing & Separation",
        "risk_score": 78,
        "risk_level": "High",
        "report_count": 290,
        "critical_reports": 26,
        "sif_precursors": 44,
        "top_hazards": ["Fire/Explosion", "Pressure Release", "Toxic Gas"],
        "lead_supervisor": "M. Saikia (Process Lead)",
        "trend": "+6% vs last month"
    },
    {
        "id": "zone-utilities",
        "name": "Utilities & Power Generation",
        "risk_score": 64,
        "risk_level": "High",
        "report_count": 145,
        "critical_reports": 11,
        "sif_precursors": 19,
        "top_hazards": ["Electrical Isolation", "Noise/Vibration", "PPE Violation"],
        "lead_supervisor": "T. Kalita (Utilities Engineer)",
        "trend": "Stable"
    },
    {
        "id": "zone-warehouse",
        "name": "Central Warehouse & Pipe Yard",
        "risk_score": 45,
        "risk_level": "Medium",
        "report_count": 110,
        "critical_reports": 4,
        "sif_precursors": 9,
        "top_hazards": ["Vehicle Interaction", "Suspended Load", "Trip Hazards"],
        "lead_supervisor": "R. Baruah (Materials Manager)",
        "trend": "-8% vs last month"
    },
    {
        "id": "zone-transport",
        "name": "Crude Transport & Logistics Fleet",
        "risk_score": 58,
        "risk_level": "Medium",
        "report_count": 160,
        "critical_reports": 8,
        "sif_precursors": 16,
        "top_hazards": ["Vehicle Interaction", "Fatigue", "Blind Spot"],
        "lead_supervisor": "K. Deka (Logistics Lead)",
        "trend": "+3% vs last month"
    }
]

# Raw seed reports
SEED_REPORTS_RAW = [
    # HERO 1: Critical Electrical Report (Exact match for SIH Scenario Step 5)
    {
        "report_id": "OIL-2048",
        "title": "Technician working on energized 415V switchgear without LOTO",
        "description": "During maintenance, the technician was working on energized electrical equipment without proper isolation.",
        "report_type": "Unsafe Act",
        "site": "Moran Wellhead A",
        "location": "Substation 3, Main Motor Control Center",
        "department": "Electrical Maintenance",
        "activity": "Electrical Switchgear Servicing",
        "reported_by": "Amit Kumar (Technician)",
        "language": "en",
        "severity": "Critical",
        "status": "Open",
        "date": "2026-09-10",
        "time": "10:35 AM",
        "people_involved": "1 Contract Electrician, 1 Apprentice",
        "equipment": "415V MCC Switchgear Panel #4",
        "immediate_action": "Supervisor verbally intervened and instructed worker to step outside boundary."
    },
    # HERO 2: Marathi Working at Height (Exact match for SIH Scenario Step 18)
    {
        "report_id": "OIL-2049",
        "title": "उंचीवर सुरक्षा पट्टा न वापरता काम (Working at height without harness)",
        "description": "कामगार सुरक्षा पट्टा न वापरता उंचीवर काम करत होता.",
        "report_type": "Unsafe Act",
        "site": "Duliajan Plant 2",
        "location": "Fractionation Column Scaffolding",
        "department": "Mechanical Maintenance",
        "activity": "Pipe Rack Structural Bolt Tightening",
        "reported_by": "S. Phukan (Safety Steward)",
        "language": "mr",
        "severity": "Critical",
        "status": "Open",
        "date": "2026-09-10",
        "time": "09:15 AM",
        "people_involved": "2 Rigging Workers",
        "equipment": "Tubular Scaffold Tower (4.2m)",
        "immediate_action": "काम थांबवण्यात आले आणि कर्मचाऱ्याला खाली बोलावले."
    },
    # HERO 3: Hindi Working at Height (Scenario match)
    {
        "report_id": "OIL-2042",
        "title": "ऊंचाई पर बिना सुरक्षा बेल्ट कार्य",
        "description": "कर्मचारी ऊंचाई पर बिना सेफ्टी बेल्ट के काम कर रहा था।",
        "report_type": "Unsafe Act",
        "site": "Digboi Rig 4",
        "location": "Derrick Monkey Board (Elevation 24m)",
        "department": "Drilling Operations",
        "activity": "Casing Stabbing Alignment",
        "reported_by": "M. Das (Floorman)",
        "language": "hi",
        "severity": "Critical",
        "status": "In Progress",
        "date": "2026-09-09",
        "time": "02:40 PM",
        "people_involved": "1 Derrickman",
        "equipment": "Rig Derrick Mast & Harness Inertia Reel",
        "immediate_action": "कार्य तत्काल रोक दिया गया और हार्नेस पहनाया गया।"
    },
    # HERO 4: Gujarati Working at Height (Scenario match)
    {
        "report_id": "OIL-2043",
        "title": "ઊંચાઈ પર સલામતી પટ્ટા વિના કામ",
        "description": "કામદાર સલામતી પટ્ટા વિના ઊંચાઈ પર કામ કરી રહ્યો હતો.",
        "report_type": "Unsafe Act",
        "site": "Moran Wellhead A",
        "location": "Header Pipe Gantry #2",
        "department": "Pipeline Integrity",
        "activity": "Ultrasonic Thickness Testing",
        "reported_by": "J. Patel (NDT Tech)",
        "language": "gu",
        "severity": "Critical",
        "status": "Pending Verification",
        "date": "2026-09-08",
        "time": "11:20 AM",
        "people_involved": "1 NDT Inspector",
        "equipment": "Temporary Aluminum Extension Ladder",
        "immediate_action": "કામદારને સલામત સ્થળે ખસેડવામાં આવ્યો."
    },
    # SIMILAR HISTORICAL REPORT 1 (Exact match for prompt Step 40: #OIL-2041)
    {
        "report_id": "OIL-2041",
        "title": "Substation feeder panel breaker serviced while busbar remained energized",
        "description": "During electrical isolation issue, technician bypassed interlock and reached into live feeder compartment.",
        "report_type": "Near Miss",
        "site": "Moran Wellhead A",
        "location": "Substation 2, Bus Coupler Bay",
        "department": "Electrical Maintenance",
        "activity": "Breaker Contact Cleaning",
        "reported_by": "P. Nath (Senior Electrical Engineer)",
        "language": "en",
        "severity": "Critical",
        "status": "Resolved",
        "date": "2026-08-28",
        "time": "03:10 PM",
        "people_involved": "1 Technician",
        "equipment": "11kV Vacuum Circuit Breaker",
        "immediate_action": "Main incoming feeder tripped remotely by SCADA."
    },
    # SIMILAR HISTORICAL REPORT 2 (Exact match for prompt Step 40: #OIL-1732)
    {
        "report_id": "OIL-1732",
        "title": "Energized panel door open without arc flash protective barriers",
        "description": "Energized panel exposure observed with terminal blocks live at 415V without insulated protective covers or warning barrier.",
        "report_type": "Unsafe Condition",
        "site": "Digboi Rig 4",
        "location": "SCR Power Control House",
        "department": "Electrical Maintenance",
        "activity": "Routine Daily Inspection",
        "reported_by": "T. Hazarika (Safety Officer)",
        "language": "en",
        "severity": "High",
        "status": "Resolved",
        "date": "2026-07-14",
        "time": "10:15 AM",
        "people_involved": "2 Contract Electricians",
        "equipment": "Main Generator Distribution Panel",
        "immediate_action": "Door closed and padlocked; hazard tape applied."
    },
    # CRITICAL ALERT 1 (Exact match for prompt Section 14)
    {
        "report_id": "OIL-2047",
        "title": "Gas leakage detected near potential ignition source",
        "description": "Gas leakage detected near potential ignition source at Moran compressor intake line while hot welding sparks flew within 5 meters.",
        "report_type": "Near Miss",
        "site": "Moran Wellhead A",
        "location": "Compressor Manifold Skid #1",
        "department": "Production & Processing",
        "activity": "Structural Skid Reinforcement Welding",
        "reported_by": "D. Roy (Gas Plant Operator)",
        "language": "en",
        "severity": "Critical",
        "status": "Open",
        "date": "2026-09-10",
        "time": "10:27 AM",
        "people_involved": "1 Welder, 1 Gas Operator",
        "equipment": "3-inch Hydrocarbon Fuel Gas Bypass Line",
        "immediate_action": "Hot work stopped immediately; valve isolated."
    },
    # CRITICAL ALERT 2 (Exact match for prompt Section 14)
    {
        "report_id": "OIL-2046",
        "title": "Electrical maintenance without documented isolation",
        "description": "Electrical maintenance without documented isolation on water injection pump booster motor terminal box.",
        "report_type": "Unsafe Act",
        "site": "Digboi Rig 4",
        "location": "Mud Pump House Substation",
        "department": "Electrical Maintenance",
        "activity": "Pump Motor Terminal Re-torquing",
        "reported_by": "B. Sharma (Instrument Tech)",
        "language": "en",
        "severity": "High",
        "status": "Assigned",
        "date": "2026-09-10",
        "time": "10:12 AM",
        "people_involved": "2 Electricians",
        "equipment": "250 HP 3-Phase Induction Motor",
        "immediate_action": "Breaker opened and tagged out."
    },
    # Confined Space Entry without testing (Hero scenario)
    {
        "report_id": "OIL-2045",
        "title": "Confined-space entry initiated without documented atmospheric testing",
        "description": "Confined-space entry initiated without documented atmospheric testing or continuous oxygen and combustible gas detector active.",
        "report_type": "Unsafe Act",
        "site": "Duliajan Plant 2",
        "location": "Crude Desalter Vessel V-101",
        "department": "Production & Processing",
        "activity": "Internal Sludge Inspection",
        "reported_by": "S. Borpatra (Shift Lead)",
        "language": "en",
        "severity": "Critical",
        "status": "In Progress",
        "date": "2026-09-09",
        "time": "04:15 PM",
        "people_involved": "3 Tank Cleaning Contractors",
        "equipment": "Horizontal Pressure Vessel V-101",
        "immediate_action": "Workers ordered out of vessel manway immediately."
    },
    # Suspended load over workers
    {
        "report_id": "OIL-2044",
        "title": "Personnel walking directly underneath 5-ton suspended drill collar load",
        "description": "Crane was lifting a heavy drill pipe bundle while two floor hands walked directly through the unbarricaded swing drop zone.",
        "report_type": "Unsafe Act",
        "site": "Digboi Rig 4",
        "location": "Rig Floor & Catwalk Area",
        "department": "Rigging & Heavy Lift",
        "activity": "Pipe Deck Loading",
        "reported_by": "N. Gogoi (Rigger Lead)",
        "language": "en",
        "severity": "Critical",
        "status": "Open",
        "date": "2026-09-08",
        "time": "01:30 PM",
        "people_involved": "Crane Operator, 2 Roustabouts",
        "equipment": "75-Ton Mobile Lattice Boom Crane",
        "immediate_action": "Load rested on deck; safety zone barricaded."
    },
    # Vehicle / Forklift interaction (Prompt Section 61)
    {
        "report_id": "OIL-2040",
        "title": "Forklift operating in pedestrian movement zone without horn",
        "description": "Forklift operating in pedestrian movement zone at excessive speed near central store exit without audible backup alarm.",
        "report_type": "Unsafe Condition",
        "site": "Duliajan Plant 2",
        "location": "Central Stores Logistics Yard",
        "department": "Logistics & Transport",
        "activity": "Drill Bit Crate Shifting",
        "reported_by": "R. Tamuly (Warehouse Keeper)",
        "language": "en",
        "severity": "High",
        "status": "Assigned",
        "date": "2026-09-07",
        "time": "11:45 AM",
        "people_involved": "Forklift Operator, Pedestrians",
        "equipment": "5-Ton Diesel Counterbalance Forklift",
        "immediate_action": "Forklift parked; reverse horn repaired."
    },
    # Additional Multilingual Reports (Hindi, Marathi, Gujarati)
    {
        "report_id": "OIL-2039",
        "title": "पाइपलाइन में गैस रिसाव देखा गया (Gas leak near welding)",
        "description": "पाइपलाइन में गैस रिसाव देखा गया और पास में वेल्डिंग का काम चल रहा था। तुरंत हॉट वर्क रुकवाया गया।",
        "report_type": "Near Miss",
        "site": "Pipeline Station C",
        "location": "Main Trunk Line Valve Station 4",
        "department": "Pipeline Integrity",
        "activity": "Pipe Support Bracket Fabrication",
        "reported_by": "A. Yadav (Safety Inspector)",
        "language": "hi",
        "severity": "Critical",
        "status": "Verified",
        "date": "2026-09-06",
        "time": "03:20 PM",
        "people_involved": "1 Welder, 1 Helper",
        "equipment": "24-inch High-Pressure Crude Gas Trunkline",
        "immediate_action": "हॉट वर्क परमिट रद्द किया गया और गैस डिटेक्टर लगाया गया।"
    },
    {
        "report_id": "OIL-2038",
        "title": "विजेच्या पॅनेलवर काम करताना पॉवर सप्लाय चालू (Live panel work)",
        "description": "विजेच्या पॅनेलवर काम करताना पॉवर सप्लाय बंद केला नव्हता. मुख्य स्वीच थेट चालू होता आणि धोका निर्माण झाला होता.",
        "report_type": "Unsafe Act",
        "site": "Naharkatiya Substation",
        "location": "Control Room Panel B",
        "department": "Electrical Maintenance",
        "activity": "Relay Testing & Calibration",
        "reported_by": "M. Joshi (Electrical Supervisor)",
        "language": "mr",
        "severity": "Critical",
        "status": "Completed",
        "date": "2026-09-05",
        "time": "10:10 AM",
        "people_involved": "2 Electricians",
        "equipment": "Transformer Secondary Protection Panel",
        "immediate_action": "पॉवर तात्काळ बंद करण्यात आली."
    },
    {
        "report_id": "OIL-2037",
        "title": "હાઇડ્રોકાર્બન લિકેજ જોવા મળ્યો (Hydrocarbon valve leak)",
        "description": "પાઇપલાઇન વાલ્વમાંથી હાઇડ્રોકાર્બન લિકેજ જોવા મળ્યો. ગેસ ડિટેક્ટર એલાર્મ વાગતા કામ અટકાવવામાં આવ્યું.",
        "report_type": "Unsafe Condition",
        "site": "Moran Wellhead A",
        "location": "Wellhead Christmas Tree Valve Block",
        "department": "Production & Processing",
        "activity": "Wellhead Flow Sampling",
        "reported_by": "P. Trivedi (Production Chemist)",
        "language": "gu",
        "severity": "Critical",
        "status": "In Progress",
        "date": "2026-09-04",
        "time": "02:15 PM",
        "people_involved": "1 Chemist",
        "equipment": "Class 1500 Flanged Gate Valve",
        "immediate_action": "વિસ્તાર ખાલી કરાવી વાલ્વ પેકિંગ ટાઈટ કરવામાં આવ્યું."
    }
]

# Generate realistic remaining reports to reach 65+ total reports
SITES = ["Moran Wellhead A", "Digboi Rig 4", "Duliajan Plant 2", "Pipeline Station C", "Naharkatiya Substation", "Numaligarh Terminal"]
DEPTS = ["Electrical Maintenance", "Mechanical Maintenance", "Drilling Operations", "Production & Processing", "Logistics & Transport", "Rigging & Heavy Lift", "Pipeline Integrity"]
TYPES = ["Unsafe Act", "Unsafe Condition", "Near Miss", "Safety Observation"]
SEVERITIES = ["Critical", "High", "Medium", "Low"]
STATUSES = ["Open", "Assigned", "In Progress", "Pending Verification", "Completed", "Verified"]

SYNTHETIC_TEMPLATES = [
    ("Unsafe scaffold board with loose binding wire on 5m access tower", "Worker observed climbing scaffold missing mid-rails and toe boards.", "Working at Height", "High", "en"),
    ("High pressure hydrotest line whip check missing on 3000 psi pump hose", "Pressurized hydrotest line had no safety cable restraints attached at union.", "Pressure Release", "Critical", "en"),
    ("Hot work grinding sparks entering unsealed drainage sumps", "Grinder throwing sparks into open trench with suspected oily residue.", "Fire/Explosion", "High", "en"),
    ("Crude oil tank sludge removal without continuous mechanical air blower", "Two workers entered storage tank with portable blower powered off.", "Confined Space", "Critical", "en"),
    ("Heavy pipe trailer reversing without banksman in congested camp road", "Semi-truck carrying 12m drill pipes backed up blind without spotter.", "Vehicle Interaction", "High", "en"),
    ("Grinder missing safety wheel guard used on structural angle iron", "Hand-held 7-inch angle grinder operating with wheel guard removed.", "Machine Safety", "Medium", "en"),
    ("Chemical transfer without face shield or chemical resistant apron", "Operative pouring biocides into water injection pit wearing only cloth gloves.", "Chemical Exposure", "High", "en"),
    ("Uncapped needle valve leaking condensate droplets on hot steam line", "Hydrocarbon condensate dripping onto 180°C steam manifold pipe.", "Fire/Explosion", "High", "en"),
    ("Crane sling with broken wires used to lift 2-ton mud motor assembly", "Wire rope sling with 6 visible wire strand breaks used for heavy lift.", "Suspended Load", "Critical", "en"),
    ("Safety goggles not worn during chipping of welding slag", "Fitter chipping welding slag with hammer without eye protection goggles.", "PPE Violation", "Low", "en"),
    ("Tripping hazard from loose electrical extension cables across walkway", "Multiple cables laid across main control room access corridor.", "General Safety Observation", "Low", "en"),
    ("Contractor entered high voltage substation yard without induction badge", "Unauthorized personnel seen in 33kV switchyard without escort.", "Electrical Isolation", "High", "en"),
    ("कमजोर मचान पर बिना हार्नेस कार्य करते हुए ठेका मजदूर", "मजदूर बिना सुरक्षा बेल्ट के 4 मीटर ऊंचे मचान पर खड़ा था।", "Working at Height", "Critical", "hi"),
    ("गैस डिटेक्टर का कैलिब्रेशन समाप्त होने के बाद भी उपयोग", "H2S मॉनिटर की कैलिब्रेशन तारीख 2 महीने पहले समाप्त हो चुकी थी।", "Confined Space", "High", "hi"),
    ("क्रेन लिफ्टिंग एरिया में बैरिकेडिंग नहीं की गई थी", "सस्पेंडेड लोड के नीचे से लोग गुजर रहे थे और कोई टैग लाइन नहीं थी।", "Suspended Load", "Critical", "hi"),
    ("विद्युत वायर का खुला जोड़ और पानी का रिसाव", "जमीन पर पड़ी बिजली की नंगी तार के पास पाइप से पानी टपक रहा था।", "Electrical Isolation", "High", "hi"),
    ("क्रेनच्या खाली कामगार उभा होता (Worker standing below crane)", "क्रेनने जड पाईप उचलला असताना कामगार थेट भाराच्या खाली उभा होता.", "Suspended Load", "Critical", "mr"),
    ("वेल्डिंग करताना अग्निशामक यंत्र उपस्थित नव्हते (No fire extinguisher)", "हॉट वर्क सुरू असताना जवळ कोणतेही फायर एक्स्टिंग्विशर ठेवले नव्हते.", "Fire/Explosion", "High", "mr"),
    ("सुरक्षा बूट न घालता प्लांटमध्ये काम (No safety boots)", "कंत्राटी कामगार चप्पल घालून प्रोसेस एरियामध्ये फिरत होता.", "PPE Violation", "Low", "mr"),
    ("ટાંકીમાં પ્રવેશતા પહેલા ગેસ તપાસ કરી નહોતી (No gas test before entry)", "કામદારો સ્ટોરેજ ટાંકીમાં ઉતર્યા ત્યારે ઓક્સિજન મીટર વાપર્યું નહોતું.", "Confined Space", "Critical", "gu"),
    ("હાઇડ્રોલિક ક્રેનનો વાયર ઘસાઈ ગયો હતો (Worn crane wire)", "ક્રેનનો સ્ટીલ વાયર ડેમેજ થયેલ હોવા છતાં પાઇપ ઉપાડવામાં આવતી હતી.", "Suspended Load", "Critical", "gu")
]

def generate_seed_reports():
    reports = list(SEED_REPORTS_RAW)
    counter = 2036
    
    for i in range(50):
        tmpl = SYNTHETIC_TEMPLATES[i % len(SYNTHETIC_TEMPLATES)]
        title, desc, hazard, sev, lang = tmpl
        site = SITES[i % len(SITES)]
        dept = DEPTS[i % len(DEPTS)]
        status = STATUSES[i % len(STATUSES)]
        days_ago = (i * 2) + 1
        dt = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        rep = {
            "report_id": f"OIL-{counter}",
            "title": f"{title} [{site[:5]}]",
            "description": f"{desc} Observed during regular morning walkaround at {site}.",
            "report_type": TYPES[i % len(TYPES)],
            "site": site,
            "location": f"Area Bay {(i % 6) + 1}, Sector {chr(65 + (i % 4))}",
            "department": dept,
            "activity": f"{hazard} Routine Maintenance",
            "reported_by": random.choice(["Amit Kumar", "S. Phukan", "P. Nath", "T. Hazarika", "R. Baruah"]),
            "language": lang,
            "severity": sev,
            "status": status,
            "date": dt,
            "time": f"{(8 + (i % 8)):02d}:{(i * 7) % 60:02d} AM",
            "people_involved": f"{(i % 3) + 1} Operations Workers",
            "equipment": f"Industrial Asset #{100 + i}",
            "immediate_action": "Work stopped and safe boundary barricaded."
        }
        reports.append(rep)
        counter -= 1
        
    return reports

# Pre-seeded corrective actions with realistic workflow progression
SEED_ACTIONS = [
    {
        "id": "act-101",
        "action_id": "ACT-2026-089",
        "report_id": "OIL-2048",
        "title": "Mandate LOTO physical isolation & zero-energy check on MCC Panel 4",
        "description": "Procure and apply master lockout padlock, attach danger tags, and perform calibrated multimeter dead-test before resuming maintenance.",
        "priority": "Critical",
        "status": "In Progress",
        "assigned_to": "Vikram Singh",
        "assigned_to_role": "Maintenance Supervisor",
        "department": "Electrical Maintenance",
        "due_date": "2026-09-15",
        "site": "Moran Wellhead A",
        "verification_required": True,
        "verification_status": "Pending",
        "verified_by": None,
        "verified_at": None,
        "notes": "LOTO kit assigned. Substation engineer attending site walk-through.",
        "created_at": "2026-09-10T10:46:00"
    },
    {
        "id": "act-102",
        "action_id": "ACT-2026-088",
        "report_id": "OIL-2049",
        "title": "Install toe-boards and enforce 100% tie-off scaffolding harness",
        "description": "Erect standard guardrails with toe boards on Column Scaffolding. Certify scaffolding green tag.",
        "priority": "Critical",
        "status": "Assigned",
        "assigned_to": "Vikram Singh",
        "assigned_to_role": "Maintenance Supervisor",
        "department": "Mechanical Maintenance",
        "due_date": "2026-09-12",
        "site": "Duliajan Plant 2",
        "verification_required": True,
        "verification_status": "Pending",
        "verified_by": None,
        "verified_at": None,
        "notes": "Scaffolders dispatched to fit edge protection.",
        "created_at": "2026-09-10T09:30:00"
    },
    {
        "id": "act-103",
        "action_id": "ACT-2026-087",
        "report_id": "OIL-2047",
        "title": "Isolate fuel gas bypass line and conduct continuous 4-gas LEL monitoring",
        "description": "Depressurize and blind off the leaking 3-inch bypass manifold. Re-test area LEL to confirm 0.0% before re-issuing hot work permit.",
        "priority": "Critical",
        "status": "Open",
        "assigned_to": "Vikram Singh",
        "assigned_to_role": "Maintenance Supervisor",
        "department": "Production & Processing",
        "due_date": "2026-09-11",
        "site": "Moran Wellhead A",
        "verification_required": True,
        "verification_status": "Pending",
        "verified_by": None,
        "verified_at": None,
        "notes": "Gas test underway by shift technician.",
        "created_at": "2026-09-10T10:30:00"
    },
    {
        "id": "act-104",
        "action_id": "ACT-2026-086",
        "report_id": "OIL-2045",
        "title": "Establish certified confined space entry attendant and rescue winch",
        "description": "Recalibrate multi-gas detector, post trained entry watchman at manway, and verify rescue tripod winch cable.",
        "priority": "Critical",
        "status": "Pending Verification",
        "assigned_to": "Vikram Singh",
        "assigned_to_role": "Maintenance Supervisor",
        "department": "Production & Processing",
        "due_date": "2026-09-14",
        "site": "Duliajan Plant 2",
        "verification_required": True,
        "verification_status": "Requested",
        "verified_by": None,
        "verified_at": None,
        "notes": "Atmospheric testing logged at 20.9% O2, 0% LEL, 0ppm H2S. Awaiting Safety Officer verification.",
        "created_at": "2026-09-09T16:30:00"
    },
    {
        "id": "act-105",
        "action_id": "ACT-2026-085",
        "report_id": "OIL-2039",
        "title": "Pipeline flange gasket replacement and ultrasonic leak check",
        "description": "Replaced damaged spiral wound gasket on Valve 4. Tested at 80 bar with soapy bubble and ultrasonic sensor.",
        "priority": "High",
        "status": "Verified",
        "assigned_to": "Vikram Singh",
        "assigned_to_role": "Maintenance Supervisor",
        "department": "Pipeline Integrity",
        "due_date": "2026-09-07",
        "site": "Pipeline Station C",
        "verification_required": True,
        "verification_status": "Verified",
        "verified_by": "Rajesh Sharma (Safety Officer)",
        "verified_at": "2026-09-07T14:20:00",
        "notes": "Ultrasonic leak test passed with zero emission.",
        "created_at": "2026-09-06T15:45:00"
    },
    {
        "id": "act-106",
        "action_id": "ACT-2026-084",
        "report_id": "OIL-2040",
        "title": "Install warehouse pedestrian bollards and repair forklift reverse horn",
        "description": "Replace faulty reverse buzzer on Forklift Unit 4 and bolt yellow heavy steel bollards around warehouse doors.",
        "priority": "High",
        "status": "Completed",
        "assigned_to": "Vikram Singh",
        "assigned_to_role": "Maintenance Supervisor",
        "department": "Logistics & Transport",
        "due_date": "2026-09-13",
        "site": "Duliajan Plant 2",
        "verification_required": True,
        "verification_status": "Pending",
        "verified_by": None,
        "verified_at": None,
        "notes": "Horn installed and tested. Walkway paint marking complete.",
        "created_at": "2026-09-07T12:00:00"
    }
]

# Notifications store
SEED_NOTIFICATIONS = [
    {
        "id": "notif-1",
        "title": "Critical SIF Precursor Detected",
        "description": "Report #OIL-2048: Energized 415V switchgear maintenance without isolation flagged with 94/100 Risk Score.",
        "timestamp": "8 minutes ago",
        "severity": "critical",
        "read": False,
        "target_type": "report",
        "target_id": "OIL-2048"
    },
    {
        "id": "notif-2",
        "title": "Action Pending Verification",
        "description": "Action #ACT-2026-086: Confined Space Pre-entry test at Duliajan Plant 2 requires Safety Officer sign-off.",
        "timestamp": "25 minutes ago",
        "severity": "high",
        "read": False,
        "target_type": "action",
        "target_id": "ACT-2026-086"
    },
    {
        "id": "notif-3",
        "title": "Recurring Hazard Signal",
        "description": "Repeat Risk Signal: Electrical isolation observations increased by +28% over the past 30 days.",
        "timestamp": "1 hour ago",
        "severity": "high",
        "read": False,
        "target_type": "intelligence",
        "target_id": "zone-maintenance"
    },
    {
        "id": "notif-4",
        "title": "Overdue Action Notice",
        "description": "Action #ACT-2026-079: Moran Wellhead pressure safety valve calibration is 2 days overdue.",
        "timestamp": "3 hours ago",
        "severity": "critical",
        "read": True,
        "target_type": "action",
        "target_id": "ACT-2026-079"
    }
]
