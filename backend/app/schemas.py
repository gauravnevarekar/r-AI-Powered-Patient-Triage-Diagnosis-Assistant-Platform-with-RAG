from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ExtractedSymptom(BaseModel):
    name: str
    severity: int = Field(..., ge=1, le=5)
    duration: str
    onset: str

class SymptomExtractRequest(BaseModel):
    free_text: str

class SymptomExtractResponse(BaseModel):
    raw_text: str
    anonymized_text: str
    extracted_symptoms: List[ExtractedSymptom]
    detected_history: List[str] = []

class MedicalHistoryItem(BaseModel):
    category: str  # e.g., 'EHR', 'Lab', 'Scan', 'Photo'
    filename: str
    extracted_text: str
    structured_findings: Dict[str, Any] = {}

class HistoryUploadResponse(BaseModel):
    session_id: str
    filename: str
    extracted_history: List[str]
    extracted_medications: List[str]
    extracted_allergies: List[str]
    anonymized_preview: str

class TriageAssessRequest(BaseModel):
    session_id: Optional[str] = "session_" + "default"
    symptom_description: str
    symptom_chips: List[str] = []
    duration: str = "< 24 hours"
    severity: int = Field(4, ge=1, le=5)
    onset: str = "Sudden onset"
    secondary_notes: Optional[str] = ""
    patient_age: Optional[int] = 30
    patient_gender: Optional[str] = "unspecified"
    dpdp_consent: bool = True

class RAGCitation(BaseModel):
    source_title: str
    guideline_ref: str
    snippet: str

class DifferentialItem(BaseModel):
    condition: str
    probability: float
    likelihood: str  # 'Likely', 'Possible', 'Unlikely'

class TriageAssessResponse(BaseModel):
    session_id: str
    urgency_level: str  # 'EMERGENCY_IMMEDIATE', 'URGENT_12_24_HRS', 'ROUTINE_CARE', 'SELF_CARE'
    urgency_title: str
    urgency_description: str
    time_window: str
    primary_condition: str
    primary_confidence: float
    differential_diagnoses: List[DifferentialItem]
    recommended_specialist: str
    care_pathway_notes: str
    clinical_reasoning: str
    rag_citations: List[RAGCitation]
    red_flag_triggered: bool
    red_flag_reason: Optional[str] = None
    cv_image_impression: Optional[str] = None
    dpdp_anonymized: bool = True

class PrescriptionQARequest(BaseModel):
    session_id: Optional[str] = "session_rx"
    prescription_name: Optional[str] = None
    question: str

class PrescriptionQAResponse(BaseModel):
    question: str
    answer: str
    safety_alert: Optional[str] = None
    source_monograph: str
    citations: List[RAGCitation]

class CareFacility(BaseModel):
    id: str
    name: str
    type: str  # 'Emergency Room', 'Urgent Care', 'Specialist Clinic', 'Dental Center', 'Maternity Hospital'
    specialists_available: List[str]
    distance_km: float
    address: str
    phone: str
    open_now: bool
    maps_url: str

class CareFinderResponse(BaseModel):
    recommended_specialist: str
    urgency_level: str
    facilities: List[CareFacility]

class PrivacyConsentRequest(BaseModel):
    session_id: str
    consent_given: bool
    allow_retention: bool = False

class GenericStatusResponse(BaseModel):
    status: str
    message: str
