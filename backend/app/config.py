import os

class Settings:
    APP_NAME: str = "HealthBridge AI Triage Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Base paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    CHROMA_DB_DIR: str = os.path.join(BASE_DIR, "chroma_db")
    
    # Privacy & DPDP Act 2023 settings
    DPDP_COMPLIANCE_MODE: bool = True
    ANONYMIZE_PII: bool = True
    DATA_RETENTION_HOURS: int = 24
    
    # RAG Settings
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    TOP_K_RETRIEVAL: int = 3

settings = Settings()
