from typing import Literal, TypedDict, Optional
from langchain_core.documents import Document
from pydantic import BaseModel, Field

class RouteDecision(BaseModel):
    source_used: Literal["kb", "direct"] = Field(
        description="Route to 'kb' for IT policy/technical questions, 'direct' for greetings."
    )

class EvidenceGrade(BaseModel):
    grade: Literal["good", "weak"] = Field(
        description="Grade 'good' if context answers the question, else 'weak'."
    )

class AgentState(TypedDict):
    question: str
    current_query: str
    kb_docs: list[Document]
    web_results: str
    kb_grade: str
    web_grade: str
    answer: str
    source_used: str
    retry_count: int
    trace: list[str]
    citations: list[str]