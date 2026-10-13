from fastapi import APIRouter, File, UploadFile, Header, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path

from app.core.config import get_settings
from app.rag.workflow import ask
from app.rag.vectorstore import add_documents
from app.services.ingestion import load_file, chunk_documents
from app.services.audit import write_audit


router = APIRouter()
settings = get_settings()

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".md"}


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=3000)


@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name
    }


@router.post("/chat")
def chat(payload: ChatRequest):
    try:
        res = ask(payload.question)

        write_audit(
            payload.question,
            res.get("source_used"),
            res.get("trace")
        )

        return {
            "answer": res.get("answer"),
            "source_used": res.get("source_used"),
            "trace": res.get("trace"),
            "citations": res.get("citations")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    x_admin_key: str = Header(...)
):

    # Allow configured admin_api_key or "change me" / "changeme" / "change-me"
    normalized_key = x_admin_key.strip().lower()
    valid_admin_keys = {
        settings.admin_api_key.strip().lower(),
        "change me",
        "change-me",
        "changeme"
    }

    if normalized_key not in valid_admin_keys:
        raise HTTPException(
            status_code=403,
            detail="Invalid admin API key"
        )

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    settings.upload_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    file_path = settings.upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    try:
        docs = load_file(file_path)

        chunks = chunk_documents(docs)

        add_documents(chunks)

        return {
            "status": "success",
            "message": f"Successfully ingested {file.filename}",
            "file": file.filename,
            "chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )