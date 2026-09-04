from fastapi import APIRouter, HTTPException
import uuid
from backend.app.schemas import (
    SymptomExtractRequest, SymptomExtractResponse,
    TriageAssessRequest, TriageAssessResponse, DifferentialItem
)
from backend.app.services.privacy_service import privacy_service
from backend.app.services.ner_service import ner_service
from backend.app.services.safety_service import safety_service
from backend.app.services.classifier_service import classifier_service
from backend.app.services.rag_service import rag_service
from backend.app.database import log_triage_session

router = APIRouter(prefix="/api/triage", tags=["Triage & Assessment"])

@router.post("/extract-symptoms", response_model=SymptomExtractResponse)
def extract_symptoms(req: SymptomExtractRequest):
    """Extract structured clinical symptoms and detected history from free text."""
    anonymized = privacy_service.anonymize_text(req.free_text)
    ner_res = ner_service.extract_symptoms(anonymized)
    
    return SymptomExtractResponse(
        raw_text=req.free_text,
        anonymized_text=anonymized,
        extracted_symptoms=ner_res["symptoms"],
        detected_history=ner_res["detected_history"]
    )

@router.post("/assess", response_model=TriageAssessResponse)
def assess_triage(req: TriageAssessRequest):
    """
    Execute full multi-stage triage assessment:
    1. DPDP Act 2023 Anonymization
    2. Medical NER & Symptom Extraction
    3. Red-Flag Safety Override Layer Check
    4. ML Multi-Disease Classification
    5. ChromaDB RAG Knowledge Base Retrieval & Source Citation Generation
    6. Database Session Logging
    """
    session_id = req.session_id if req.session_id and req.session_id != "session_default" else f"sess_{uuid.uuid4().hex[:8]}"
    
    # 1. Privacy Anonymization
    clean_desc = privacy_service.anonymize_text(req.symptom_description)
    clean_notes = privacy_service.anonymize_text(req.secondary_notes or "")
    
    # 2. Red-Flag Safety Engine Evaluation
    full_text = f"{clean_desc} {clean_notes} {' '.join(req.symptom_chips)}"
    red_flag_triggered, red_flag_reason, red_flag_urgency = safety_service.evaluate_safety_override(full_text, req.severity)
    
    # 3. ML Multi-Disease Classification
    ml_res = classifier_service.predict(clean_desc, req.symptom_chips)
    
    primary_condition = ml_res["primary_condition"]
    confidence = ml_res["primary_confidence"]
    specialist = ml_res["specialist"]
    
    # Determine Final Urgency Level (Red-Flag override takes absolute precedence)
    if red_flag_triggered:
        urgency_level = "EMERGENCY_IMMEDIATE"
        urgency_title = "SEEK IMMEDIATE EMERGENCY CARE (DIAL 911 / GO TO ER)"
        urgency_desc = red_flag_reason or "Critical safety alert triggered due to severe red-flag symptom combination."
        time_window = "Immediate (< 1 Hour)"
    else:
        urgency_level = ml_res["urgency"]
        if urgency_level == "URGENT_12_24_HRS":
            urgency_title = "SEEK TIMELY CARE — SEE A DOCTOR WITHIN 12-24 HOURS"
            urgency_desc = "Acute localized symptoms warrant prompt physical evaluation to prevent escalation."
            time_window = "12–24 Hours"
        elif urgency_level == "ROUTINE_CARE":
            urgency_title = "SCHEDULE ROUTINE CLINICAL EVALUATION"
            urgency_desc = "Symptoms suggest a manageable subacute condition. Consult a primary physician within 2-5 days."
            time_window = "2–5 Days"
        else:
            urgency_title = "SELF-CARE & AMBULATORY MONITORING"
            urgency_desc = "Mild self-limiting presentation. Monitor symptoms at home and rest."
            time_window = "3–7 Days Monitoring"

    # 4. RAG Clinical Knowledge Retrieval & Evidence Citations
    rag_res = rag_service.retrieve_and_generate(primary_condition, full_text)
    
    # 5. Format Differentials
    differentials = [DifferentialItem(**d) for d in ml_res["differential_diagnoses"]]

    # 6. Database Logging
    log_triage_session(
        session_id=session_id,
        symptoms_text=clean_desc,
        predicted_condition=primary_condition,
        urgency_level=urgency_level,
        red_flag_triggered=red_flag_triggered,
        consent_given=req.dpdp_consent
    )

    return TriageAssessResponse(
        session_id=session_id,
        urgency_level=urgency_level,
        urgency_title=urgency_title,
        urgency_description=urgency_desc,
        time_window=time_window,
        primary_condition=primary_condition,
        primary_confidence=confidence,
        differential_diagnoses=differentials,
        recommended_specialist=specialist,
        care_pathway_notes=f"Recommended evaluation by a {specialist}. Relevant lab or diagnostic markers recommended based on clinical presentation.",
        clinical_reasoning=rag_res["reasoning"],
        rag_citations=rag_res["citations"],
        red_flag_triggered=red_flag_triggered,
        red_flag_reason=red_flag_reason,
        cv_image_impression="Ultrasound / Scan summary interpretation available if records attached.",
        dpdp_anonymized=True
    )
