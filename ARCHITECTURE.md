# System Architecture - HealthBridge AI Triage & Diagnosis Platform

## End-to-End Core Pipeline Flow

1. **Patient Intake & Document OCR**:
   - Free text or guided symptom inputs, severity (1-5), duration, and onset pattern.
   - Optional upload of past lab reports, discharge summaries, or scan images.
2. **Privacy Anonymization Engine**:
   - PII/PHI redaction enforcing India DPDP Act 2023.
3. **Medical NER & Symptom Extraction**:
   - Normalizing free-text symptoms into structured clinical entities.
4. **General Red-Flag Safety Override Layer**:
   - Rule-based safety check enforcing immediate ER urgency for critical symptom combinations (crushing chest pain, severe preeclampsia signs, subarachnoid hemorrhage headache).
5. **Unified Multi-Disease ML Classifier**:
   - TF-IDF + Random Forest model trained on 50+ conditions across general medicine, emergency care, dental, and pregnancy.
6. **RAG-Grounded Clinical Reasoning (ChromaDB + Vector Store)**:
   - Chunked knowledge base (WHO, MedlinePlus, ACOG, ADA) retrieved for clinical reasoning with source citations.
7. **Prescription Q&A RAG Engine**:
   - Pharmacology database querying for drug interactions, side effects, and administration advice.
8. **Nearby Care Finder**:
   - Locate-and-inform service finding nearest ERs, urgent care clinics, surgical suites, and specialists matching triage recommendations.
