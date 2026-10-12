from langchain_core.documents import Document
from typing_extensions import TypedDict
from pydantic import BaseModel,Field
from typing import  Literal,Optional,List

class RouteDecision(BaseModel):
    route:Literal["kb","direct"]=Field(
        description="use Kb for available in agentic rag doc; direct for greeting/simple chat "
    )

class EvidenceGrade(BaseModel):
    grade:Literal["good","weak"]=Field(
        description="good mean evidence can answere the question ; weak means not enough evidence"
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
    citation: list[dict]
    retry_count: int