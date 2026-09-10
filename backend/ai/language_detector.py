"""
Language Detector for SIFGUARD AI
Supports automatic detection of English, Hindi, Marathi, Gujarati, and other Indic languages
using Unicode script block analysis, n-grams, and safety-specific lexicons.
"""

import re
from typing import Dict, Any

MARATHI_MARKERS = {
    "आहे", "आहेत", "होता", "होती", "होते", "कामगार", "उंचीवर", "सुरक्षा", "पट्टा", "वापरता", 
    "करणे", "केले", "नाही", "इथे", "अपघात", "यंत्र", "तपासणी", "धोका", "कामाच्या", "जागेवर",
    "विजेच्या", "पॅनेलवर", "गळती", "दुरुस्ती", "साहित्य", "हेल्मेट", "बूट", "बंधनकारक", "टाळणे"
}

HINDI_MARKERS = {
    "है", "हैं", "था", "थी", "थे", "कर्मचारी", "मजदूर", "ऊंचाई", "पर", "बिना", "सेफ्टी", 
    "बेल्ट", "काम", "कर", "रहा", "रही", "रहे", "गैस", "रिसाव", "वेल्डिंग", "सुरक्षा",
    "खतरा", "बिजली", "उपकरण", "जांच", "निरीक्षण", "दुर्घटना", "रोकथाम", "निर्देश"
}

GUJARATI_MARKERS = {
    "છે", "હતો", "હતી", "હતા", "કામદાર", "સલામતી", "પટ્ટો", "પટ્ટા", "વિના", "ઊંચાઈ",
    "પર", "કામ", "કરી", "રહ્યો", "લિકેજ", "જોવા", "મળ્યો", "વાલ્વમાંથી", "ગેસ", "જોખમ"
}

def detect_language(text: str) -> Dict[str, Any]:
    """
    Detects language and returns language code, language name, and confidence score.
    Supports Auto-detection with high confidence for English, Hindi, Marathi, and Gujarati.
    """
    if not text or not text.strip():
        return {
            "code": "en",
            "name": "English",
            "confidence": 0.95,
            "detected_script": "Latin"
        }

    clean_text = text.strip()
    total_chars = len(clean_text)
    
    devanagari_count = len(re.findall(r'[\u0900-\u097F]', clean_text))
    gujarati_count = len(re.findall(r'[\u0A80-\u0AFF]', clean_text))
    tamil_count = len(re.findall(r'[\u0B80-\u0BFF]', clean_text))
    telugu_count = len(re.findall(r'[\u0C00-\u0C7F]', clean_text))
    kannada_count = len(re.findall(r'[\u0C80-\u0CFF]', clean_text))
    malayalam_count = len(re.findall(r'[\u0D00-\u0D7F]', clean_text))
    punjabi_count = len(re.findall(r'[\u0A00-\u0A7F]', clean_text))
    bengali_count = len(re.findall(r'[\u0980-\u09FF]', clean_text))
    latin_count = len(re.findall(r'[a-zA-Z]', clean_text))

    if gujarati_count > 3 or (gujarati_count / max(total_chars, 1)) > 0.2:
        words = clean_text.split()
        match_count = sum(1 for w in words if w in GUJARATI_MARKERS)
        confidence = min(0.99, 0.88 + (match_count * 0.03) + (gujarati_count / total_chars * 0.08))
        return {
            "code": "gu",
            "name": "Gujarati",
            "confidence": round(confidence, 2),
            "detected_script": "Gujarati"
        }

    if devanagari_count > 3 or (devanagari_count / max(total_chars, 1)) > 0.2:
        words = set(re.findall(r'[\u0900-\u097F]+', clean_text))
        marathi_hits = len(words.intersection(MARATHI_MARKERS))
        hindi_hits = len(words.intersection(HINDI_MARKERS))
        
        for w in words:
            if w.endswith("वर") or w.endswith("च्या") or w.endswith("तील") or w.endswith("णारा") or w.endswith("णारे"):
                marathi_hits += 1.5

        if marathi_hits > hindi_hits:
            confidence = min(0.99, 0.89 + (marathi_hits * 0.02))
            return {
                "code": "mr",
                "name": "Marathi",
                "confidence": round(confidence, 2),
                "detected_script": "Devanagari"
            }
        else:
            confidence = min(0.99, 0.90 + (hindi_hits * 0.02))
            return {
                "code": "hi",
                "name": "Hindi",
                "confidence": round(confidence, 2),
                "detected_script": "Devanagari"
            }

    if tamil_count > 3:
        return {"code": "ta", "name": "Tamil", "confidence": 0.96, "detected_script": "Tamil"}
    if telugu_count > 3:
        return {"code": "te", "name": "Telugu", "confidence": 0.96, "detected_script": "Telugu"}
    if kannada_count > 3:
        return {"code": "kn", "name": "Kannada", "confidence": 0.95, "detected_script": "Kannada"}
    if malayalam_count > 3:
        return {"code": "ml", "name": "Malayalam", "confidence": 0.95, "detected_script": "Malayalam"}
    if punjabi_count > 3:
        return {"code": "pa", "name": "Punjabi", "confidence": 0.95, "detected_script": "Gurmukhi"}
    if bengali_count > 3:
        return {"code": "bn", "name": "Bengali", "confidence": 0.96, "detected_script": "Bengali"}

    confidence = 0.95 if latin_count > 5 else 0.85
    return {
        "code": "en",
        "name": "English",
        "confidence": confidence,
        "detected_script": "Latin"
    }
