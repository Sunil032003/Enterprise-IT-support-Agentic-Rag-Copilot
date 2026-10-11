from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root directory
# Adjust parents[2] if your config.py is located at a different depth.
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # --------------------------------------------------
    # Application
    # --------------------------------------------------
    app_name: str = "Enterprise IT Support Agentic RAG Copilot"
    app_env: str = "development"

    # --------------------------------------------------
    # API Keys
    # --------------------------------------------------
    gemini_api_key: str = ""
    tavily_api_key: str = ""
    pinecone_api_key: str = ""

    # --------------------------------------------------
    # Pinecone
    # --------------------------------------------------
    pinecone_index_name: str = "sample_knowledgebase"
    pinecone_namespace: str = "company-it-support"

    # --------------------------------------------------
    # LLM / Embeddings
    # --------------------------------------------------
    gemini_model: str = "gemini-3.8-flash"
    embedding_model: str = "gemini-embedding-001"

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------
    top_k: int = 4
    max_retries: int = 1

    # --------------------------------------------------
    # Admin
    # --------------------------------------------------
    admin_api_key: str = ""

    # --------------------------------------------------
    # Paths
    # --------------------------------------------------
    audit_db_path: str = str(BASE_DIR / "data" / "audit.db")
    uploads_dir: str = str(BASE_DIR / "uploads")
    sample_kb_path: str = str(BASE_DIR / "data" / "sample_kb")

    # --------------------------------------------------
    # Pydantic Settings
    # --------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
       return Settings()

