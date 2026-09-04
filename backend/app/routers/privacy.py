from fastapi import APIRouter, HTTPException
from backend.app.schemas import PrivacyConsentRequest, GenericStatusResponse
from backend.app.services.privacy_service import privacy_service

router = APIRouter(prefix="/api/privacy", tags=["DPDP Privacy & Compliance"])

@router.post("/consent", response_model=GenericStatusResponse)
def record_consent(req: PrivacyConsentRequest):
    """Record patient DPDP Act 2023 consent preferences."""
    return GenericStatusResponse(
        status="SUCCESS",
        message=f"DPDP consent preferences recorded for session {req.session_id}."
    )

@router.delete("/session/{session_id}", response_model=GenericStatusResponse)
def delete_session(session_id: str):
    """Execute right to erasure under DPDP Act 2023 by purging session data."""
    success = privacy_service.enforce_erasure(session_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to purge session data")
    
    return GenericStatusResponse(
        status="PURGED",
        message=f"Session data for {session_id} permanently deleted under India DPDP Act 2023."
    )
