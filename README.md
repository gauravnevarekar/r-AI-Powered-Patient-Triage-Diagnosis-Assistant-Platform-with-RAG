# HealthBridge AI: AI-Powered Patient Triage & Diagnosis Assistant Platform with RAG

A patient-facing AI platform for symptom analysis, source-grounded clinical triage explanations, red-flag safety overrides, prescription Q&A, and nearby care navigation, fully compliant with **India's DPDP Act 2023**.

---

## Key Features

1. **Patient Intake & Document OCR**: Free-text symptom input, duration, severity scale, and upload of lab PDFs or scan images.
2. **India DPDP Act 2023 Compliance**: PII/PHI scrubbing, explicit consent recording, and one-click session data erasure.
3. **Unified Multi-Disease ML Classifier**: Trained on 50+ conditions across General Medicine, Dental, Pregnancy/Gynecology, and Emergency Care.
4. **General Red-Flag Safety Override**: Rule-based safety layer enforcing Immediate ER urgency for critical symptoms regardless of ML confidence.
5. **RAG Clinical Reasoning (ChromaDB + Vector DB)**: Source-grounded clinical explanations citing WHO, MedlinePlus, ACOG, and ADA guidelines.
6. **Prescription Q&A (RAG-Powered)**: Pharmacology database query engine answering patient questions regarding drug interactions, side effects, and administration advice.
7. **Nearby Care Finder**: Locate-and-inform service mapping recommended specialists to nearby urgent care centers, ERs, dental clinics, or maternity hospitals.

---

## Quick Start & Execution Guide

### 1. Launch FastAPI Server Locally
```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```
- Web Application UI: `http://localhost:8000/static/index.html` or `http://localhost:8000`
- Interactive OpenAPI / Swagger Docs: `http://localhost:8000/docs`

### 2. Execute ML Classifier Performance Evaluation
```bash
python -m backend.evaluation.evaluate_classifier
```
*Calculates per-class Precision, Recall, F1, and critical False Negative Rate (FNR) on urgent emergency conditions.*

### 3. Execute RAG Retrieval & Grounding Evaluation
```bash
python -m backend.evaluation.evaluate_rag
```
*Measures RAG retrieval Precision@1 and zero-hallucination source citation verification.*

### 4. Run Pytest Suite
```bash
pytest backend/tests/
```

---

## API Endpoint Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/triage/extract-symptoms` | Medical NER symptom extraction from free text |
| `POST` | `/api/triage/assess` | Executes full intake assessment (NER -> ML -> Red-Flag -> RAG) |
| `POST` | `/api/history/upload` | Upload & OCR process lab reports or scan images |
| `POST` | `/api/rx/qa` | Prescription Q&A powered by pharmacology RAG |
| `GET`  | `/api/care/nearby` | Find nearby care centers matching recommended specialist |
| `DELETE` | `/api/privacy/session/{id}` | Execute DPDP Act 2023 right to erasure data deletion |

---

## Deployment with Docker

```bash
docker-compose up --build
```
