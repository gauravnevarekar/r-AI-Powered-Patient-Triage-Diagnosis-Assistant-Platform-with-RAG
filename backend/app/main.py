import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.app.config import settings
from backend.app.routers import triage, history, rx, care, privacy

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Patient Triage & Diagnosis Assistant Platform with RAG, Privacy Compliance (DPDP Act 2023), and Multimodal Care Navigation",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(triage.router)
app.include_router(history.router)
app.include_router(rx.router)
app.include_router(care.router)
app.include_router(privacy.router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mount js directory and static files
js_dir = os.path.join(BASE_DIR, "js")
if os.path.exists(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")

if os.path.exists(BASE_DIR):
    app.mount("/static", StaticFiles(directory=BASE_DIR, html=True), name="static")

@app.get("/")
def read_root():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "ONLINE",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "HEALTHY", "model_loaded": True}
