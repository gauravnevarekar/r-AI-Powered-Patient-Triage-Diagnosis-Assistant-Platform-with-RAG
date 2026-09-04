from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import uuid
from backend.app.schemas import HistoryUploadResponse
from backend.app.services.doc_service import doc_service
from backend.app.services.privacy_service import privacy_service

router = APIRouter(prefix="/api/history", tags=["Medical History & Documents"])

@router.post("/upload", response_model=HistoryUploadResponse)
async def upload_medical_record(
    file: UploadFile = File(...),
    category: str = Form("labs"),
    session_id: str = Form("default_session")
):
    """Upload and process medical history PDFs, lab reports, or scan images."""
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    content = await file.read()
    res = doc_service.process_file(file.filename, content, file.content_type)
    
    anonymized_preview = privacy_service.anonymize_text(res["extracted_text"])
    
    return HistoryUploadResponse(
        session_id=session_id if session_id != "default_session" else f"sess_{uuid.uuid4().hex[:8]}",
        filename=file.filename,
        extracted_history=res["extracted_history"],
        extracted_medications=res["extracted_medications"],
        extracted_allergies=res["extracted_allergies"],
        anonymized_preview=anonymized_preview
    )
