import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "HEALTHY"

def test_extract_symptoms_ner():
    payload = {"free_text": "I have severe sharp lower right abdominal pain and nausea for 12 hours."}
    response = client.post("/api/triage/extract-symptoms", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["extracted_symptoms"]) > 0
    assert data["anonymized_text"] is not None

def test_triage_assess_normal():
    payload = {
        "symptom_description": "Persistent dry cough, mild chest tightness, low fever for 3 days.",
        "symptom_chips": ["Persistent cough", "Fever"],
        "severity": 3,
        "duration": "1-3 days",
        "onset": "Gradual worsening"
    }
    response = client.post("/api/triage/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "primary_condition" in data
    assert "urgency_level" in data
    assert len(data["rag_citations"]) > 0

def test_red_flag_safety_override():
    payload = {
        "symptom_description": "Sudden severe crushing chest pain radiating to left arm with shortness of breath.",
        "symptom_chips": ["Chest pain", "Shortness of breath"],
        "severity": 5,
        "duration": "< 24 hours",
        "onset": "Sudden onset"
    }
    response = client.post("/api/triage/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["red_flag_triggered"] is True
    assert data["urgency_level"] == "EMERGENCY_IMMEDIATE"

def test_xray_image_upload_classification():
    from PIL import Image, ImageDraw
    import io
    img = Image.new("L", (224, 224), color=30)
    draw = ImageDraw.Draw(img)
    draw.ellipse([80, 40, 140, 180], fill=150)
    draw.ellipse([30, 45, 95, 170], fill=45)
    draw.ellipse([130, 45, 195, 170], fill=45)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    response = client.post(
        "/api/history/upload",
        files={"file": ("chest_xray_sample.png", buf, "image/png")},
        data={"category": "imaging", "session_id": "test_sess_img"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "chest_xray_sample.png" in data["filename"]
    assert "CNN" in data["anonymized_preview"] or "Image" in data["anonymized_preview"]

