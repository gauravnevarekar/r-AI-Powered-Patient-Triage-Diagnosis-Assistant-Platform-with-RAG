import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_prescription_qa_rag():
    payload = {
        "prescription_name": "Amoxicillin-Clavulanate",
        "question": "Can I take this with paracetamol?"
    }
    response = client.post("/api/rx/qa", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "paracetamol" in data["answer"].lower()
    assert len(data["citations"]) > 0

def test_care_finder_endpoint():
    response = client.get("/api/care/nearby?specialist=General Surgeon&urgency=URGENT_12_24_HRS")
    assert response.status_code == 200
    data = response.json()
    assert len(data["facilities"]) > 0

def test_privacy_erasure_dpdp():
    session_id = "test_sess_123"
    response = client.delete(f"/api/privacy/session/{session_id}")
    assert response.status_code == 200
    assert response.json()["status"] == "PURGED"
