from typing import Tuple, Optional

class RedFlagSafetyService:
    def __init__(self):
        # Critical red-flag symptom combinations across domains
        self.red_flag_rules = [
            # Cardiology / Emergency
            {
                "keywords": ["chest pain", "shortness of breath"],
                "reason": "Crushing chest pain paired with shortness of breath suggests high risk of Acute Coronary Syndrome or Pulmonary Embolism."
            },
            {
                "keywords": ["chest pain", "left arm"],
                "reason": "Chest pain radiating to the left arm is a classic red-flag indicator for acute myocardial infarction."
            },
            # Neurology
            {
                "keywords": ["thunderclap", "headache"],
                "reason": "Sudden severe 'thunderclap' headache reaching peak intensity instantly requires emergency CT to rule out Subarachnoid Hemorrhage."
            },
            {
                "keywords": ["facial drooping", "arm weakness"],
                "reason": "Acute unilateral facial drooping or arm weakness is a red-flag sign of Acute Ischemic Stroke."
            },
            {
                "keywords": ["stiff neck", "high fever", "headache"],
                "reason": "Combination of high fever, severe headache, and nuchal rigidity (stiff neck) indicates suspected Acute Meningitis."
            },
            # Pregnancy / Obstetrics
            {
                "keywords": ["vaginal bleeding", "pelvic pain"],
                "reason": "Vaginal bleeding paired with pelvic pain in pregnancy indicates emergency risk of Ectopic Pregnancy or Threatened Miscarriage."
            },
            {
                "keywords": ["high blood pressure", "severe headache", "vision"],
                "reason": "High blood pressure with persistent severe headache and visual changes in pregnancy indicates severe Preeclampsia."
            },
            # Surgery / Abdomen
            {
                "keywords": ["severe pain", "lower right abdomen", "fever"],
                "reason": "Severe lower right abdominal pain with fever indicates acute peritoneal irritation / suspected appendiceal rupture risk."
            },
            # Anaphylaxis
            {
                "keywords": ["throat tightness", "wheezing"],
                "reason": "Throat tightness paired with wheezing signals acute Anaphylaxis risk requiring emergency epinephrine."
            }
        ]

    def evaluate_safety_override(self, symptoms_text: str, severity: int) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Evaluates input text against red-flag clinical rules.
        Returns: (is_red_flag_triggered, red_flag_reason, recommended_urgency)
        """
        text_lower = symptoms_text.lower()

        # Rule 1: Severity 5 is automatically an immediate emergency
        if severity >= 5:
            return True, "Patient reported Level 5 (Unbearable/Agonizing) severity requiring immediate emergent evaluation.", "EMERGENCY_IMMEDIATE"

        # Rule 2: Check multi-keyword clinical safety rules
        for rule in self.red_flag_rules:
            keywords = rule["keywords"]
            if all(kw in text_lower for kw in keywords):
                return True, rule["reason"], "EMERGENCY_IMMEDIATE"

        return False, None, None

safety_service = RedFlagSafetyService()
