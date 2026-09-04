import re
import sqlite3
from backend.app.database import delete_session_record

class PrivacyService:
    def __init__(self):
        # Patterns for scrubbing PII under DPDP Act 2023
        self.phone_pattern = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self.aadhaar_pattern = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b')
        self.ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

    def anonymize_text(self, text: str) -> str:
        """Scrub PII and PHI identifiers from patient text to conform with India's DPDP Act 2023."""
        if not text:
            return ""
        
        scrubbed = text
        scrubbed = self.phone_pattern.sub('[PHONE_REDACTED]', scrubbed)
        scrubbed = self.email_pattern.sub('[EMAIL_REDACTED]', scrubbed)
        scrubbed = self.aadhaar_pattern.sub('[GOVT_ID_REDACTED]', scrubbed)
        scrubbed = self.ssn_pattern.sub('[SSN_REDACTED]', scrubbed)
        
        return scrubbed

    def enforce_erasure(self, session_id: str) -> bool:
        """Executes right to erasure under DPDP Act 2023 by purging session data."""
        try:
            delete_session_record(session_id)
            return True
        except Exception as e:
            print(f"Error purging session data for {session_id}: {e}")
            return False

privacy_service = PrivacyService()
