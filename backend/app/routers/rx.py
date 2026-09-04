from fastapi import APIRouter, HTTPException
from backend.app.schemas import PrescriptionQARequest, PrescriptionQAResponse
from backend.app.services.rx_rag_service import rx_rag_service

router = APIRouter(prefix="/api/rx", tags=["Prescription Q&A (RAG)"])

@router.post("/qa", response_model=PrescriptionQAResponse)
def prescription_qa(req: PrescriptionQARequest):
    """Answer patient questions regarding prescriptions using drug monograph RAG."""
    drug_name = req.prescription_name or "Amoxicillin-Clavulanate"
    res = rx_rag_service.answer_question(drug_name, req.question)
    
    return PrescriptionQAResponse(
        question=req.question,
        answer=res["answer"],
        safety_alert=res["safety_alert"],
        source_monograph=res["source_monograph"],
        citations=res["citations"]
    )
