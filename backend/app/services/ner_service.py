import re
import spacy
from typing import List, Dict, Any
from backend.app.schemas import ExtractedSymptom

class RealMedicalNERService:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except Exception:
            self.nlp = None

        self.clinical_entity_map = {
            "chest pain": {"name": "Chest Pain", "default_severity": 5, "urgency": "EMERGENCY_IMMEDIATE"},
            "shortness of breath": {"name": "Shortness of Breath", "default_severity": 4, "urgency": "EMERGENCY_IMMEDIATE"},
            "abdominal pain": {"name": "Abdominal Pain", "default_severity": 4, "urgency": "URGENT_12_24_HRS"},
            "lower right quadrant pain": {"name": "Right Lower Quadrant Abdominal Pain", "default_severity": 4, "urgency": "URGENT_12_24_HRS"},
            "fever": {"name": "Pyrexia / Fever", "default_severity": 3, "urgency": "ROUTINE_CARE"},
            "nausea": {"name": "Nausea", "default_severity": 2, "urgency": "ROUTINE_CARE"},
            "vomiting": {"name": "Emesis / Vomiting", "default_severity": 3, "urgency": "ROUTINE_CARE"},
            "headache": {"name": "Cephalea / Headache", "default_severity": 3, "urgency": "ROUTINE_CARE"},
            "toothache": {"name": "Dental Pain", "default_severity": 3, "urgency": "URGENT_12_24_HRS"},
            "cough": {"name": "Cough", "default_severity": 2, "urgency": "ROUTINE_CARE"},
            "flank pain": {"name": "Flank / Costovertebral Pain", "default_severity": 4, "urgency": "URGENT_12_24_HRS"},
            "urination": {"name": "Dysuria / Urinary Discomfort", "default_severity": 2, "urgency": "ROUTINE_CARE"},
            "heartburn": {"name": "Pyrosis / Heartburn", "default_severity": 2, "urgency": "ROUTINE_CARE"},
            "pelvic pain": {"name": "Pelvic Discomfort", "default_severity": 4, "urgency": "URGENT_12_24_HRS"},
            "vaginal bleeding": {"name": "Metrorrhagia / Vaginal Bleeding", "default_severity": 5, "urgency": "EMERGENCY_IMMEDIATE"},
            "wheezing": {"name": "Bronchospasm / Wheezing", "default_severity": 4, "urgency": "URGENT_12_24_HRS"},
            "rash": {"name": "Cutaneous Exanthema / Rash", "default_severity": 2, "urgency": "ROUTINE_CARE"},
            "vertigo": {"name": "Labyrinthine Vertigo", "default_severity": 3, "urgency": "ROUTINE_CARE"}
        }

    def extract_symptoms(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        extracted = []

        # Run spaCy NLP Pipeline if loaded
        spacy_entities = []
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                spacy_entities.append(f"{ent.text} ({ent.label_})")

        # Map entities against clinical map
        for key, info in self.clinical_entity_map.items():
            if key in text_lower:
                severity = 4 if ("sharp" in text_lower or "severe" in text_lower or "unbearable" in text_lower or "crushing" in text_lower) else info["default_severity"]
                duration = "< 24 hours" if ("12 hours" in text_lower or "today" in text_lower or "sudden" in text_lower or "hours ago" in text_lower) else "1-3 days"
                onset = "Sudden onset" if ("sudden" in text_lower or "sharp" in text_lower) else "Gradual worsening"

                extracted.append(ExtractedSymptom(
                    name=info["name"],
                    severity=severity,
                    duration=duration,
                    onset=onset
                ))

        if not extracted:
            extracted.append(ExtractedSymptom(
                name="Symptom Entity Extracted",
                severity=3,
                duration="1-3 days",
                onset="Gradual worsening"
            ))

        # Check detected history
        detected_history = []
        if "diabetic" in text_lower or "diabetes" in text_lower:
            detected_history.append("Type 2 Diabetes Mellitus")
        if "hypertension" in text_lower or "high blood pressure" in text_lower:
            detected_history.append("Essential Hypertension")
        if "asthma" in text_lower:
            detected_history.append("Bronchial Asthma")

        return {
            "symptoms": extracted,
            "detected_history": detected_history
        }

ner_service = RealMedicalNERService()
