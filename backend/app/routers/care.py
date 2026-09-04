from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas import CareFinderResponse
from backend.app.services.care_finder_service import care_finder_service

router = APIRouter(prefix="/api/care", tags=["Nearby Care Finder"])

@router.get("/nearby", response_model=CareFinderResponse)
def get_nearby_care(
    specialist: str = Query("General Surgeon", description="Specialist type recommended"),
    urgency: str = Query("URGENT_12_24_HRS", description="Assessed urgency level"),
    lat: Optional[float] = Query(None, description="Patient real latitude"),
    lng: Optional[float] = Query(None, description="Patient real longitude")
):
    """Find real nearby healthcare facilities matching recommended specialist and patient GPS location."""
    return care_finder_service.find_nearby(specialist, urgency, lat=lat, lng=lng)
