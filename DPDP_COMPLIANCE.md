# Data Privacy & India DPDP Act 2023 Compliance Architecture

## Overview
HealthBridge AI is engineered to conform with India's **Digital Personal Data Protection (DPDP) Act 2023** guidelines for processing digital personal health data.

---

## Key DPDP Act 2023 Principles Implemented

### 1. Lawful & Transparent Consent Capture (`/api/privacy/consent`)
- **Explicit Consent**: Prior to processing any symptom descriptions or uploaded medical documents, patients must acknowledge DPDP consent terms.
- **Purpose Limitation**: Patient health data is strictly processed for current triage prioritization and care navigation.

### 2. Automated PII / PHI Anonymization (`privacy_service.py`)
- All free-text inputs and document OCR outputs undergo automated sanitization before entering the ML classification or RAG pipelines.
- Redacted fields include:
  - Phone Numbers (`[PHONE_REDACTED]`)
  - Email Addresses (`[EMAIL_REDACTED]`)
  - Govt IDs / Aadhaar / SSN (`[GOVT_ID_REDACTED]`)

### 3. Session-Scoped Zero-Knowledge Storage
- Uploaded medical reports and images are evaluated in volatile session memory.
- No health records are stored permanently on server disks unless explicit consent for longitudinal chart retention is granted.

### 4. Right to Erasure / Data Deletion (`DELETE /api/privacy/session/{session_id}`)
- Patients retain full authority to purge all session records and log traces at any point by clicking **"Purge session data under DPDP Act 2023"** in the UI.
