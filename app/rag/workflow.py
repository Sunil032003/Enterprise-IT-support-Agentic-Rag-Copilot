from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from app.core.config import get_settings
from app.rag.state import AgentState, RouteDecision, EvidenceGrade
from app.rag.vectorstore import get_retriever

settings = get_settings()
_llm = None
_web_search = None

def get_text(response):
    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict)
        )

    return str(content)

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.gemini_api_key,
            temperature=0
        )
    return _llm

def get_web_search():
    global _web_search
    if _web_search is None:
        _web_search = TavilySearchResults(
            tavily_api_key=settings.tavily_api_key,
            max_results=5
        )
    return _web_search

# Node functions
def route_question(state: AgentState):
    llm = get_llm().with_structured_output(RouteDecision)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an IT support router. Route to 'kb' for IT policies/VPN/MFA queries, or 'direct' for greetings."),
        ("human", "{question}")
    ])
    res = llm.invoke(prompt.format_messages(question=state["question"]))
    state["source_used"] = res.source_used
    state["trace"].append(f"Routed to: {res.source_used}")
    return state

def retrieve_kb(state: AgentState):
    retriever = get_retriever()
    docs = retriever.invoke(state["current_query"])
    state["kb_docs"] = docs
    state["trace"].append(f"Retrieved {len(docs)} docs from Pinecone KB.")
    return state

def grade_kb_evidence(state: AgentState):
    llm = get_llm().with_structured_output(EvidenceGrade)
    context = "\n\n".join([d.page_content for d in state["kb_docs"]])
    prompt = ChatPromptTemplate.from_template("Question: {q}\n\nContext:\n{c}\n\nDoes context answer question? Grade good or weak.")
    res = llm.invoke(prompt.format_messages(q=state["question"], c=context))
    state["kb_grade"] = res.grade
    state["trace"].append(f"KB Evidence Graded: {res.grade}")
    return state

def web_search(state: AgentState):
    tool = get_web_search()
    results = tool.invoke({"query": state["current_query"]})
    state["web_results"] = str(results)
    state["trace"].append("Performed Tavily web search.")
    return state

def grade_web_evidence(state: AgentState):
    llm = get_llm().with_structured_output(EvidenceGrade)
    prompt = ChatPromptTemplate.from_template("Question: {q}\n\nWeb Results:\n{w}\n\nGrade web results as good or weak.")
    res = llm.invoke(prompt.format_messages(q=state["question"], w=state["web_results"]))
    state["web_grade"] = res.grade
    state["trace"].append(f"Web Evidence Graded: {res.grade}")
    return state

def rewrite_query(state: AgentState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("Rewrite this IT query for better search retrieval: {q}")
    res = llm.invoke(prompt.format_messages(q=state["current_query"]))

    rewritten_query = get_text(res)

    state["current_query"] = rewritten_query
    state["retry_count"] += 1
    state["trace"].append(f"Rewrote query: {rewritten_query}")
    return state

def generate_kb_answer(state: AgentState):
    llm = get_llm()
    context = "\n\n".join([d.page_content for d in state["kb_docs"]])
    prompt = ChatPromptTemplate.from_template("Answer based on internal IT docs:\n{c}\n\nQuestion: {q}")
    res = llm.invoke(prompt.format_messages(c=context, q=state["question"]))
    state["answer"] = get_text(res)
    state["citations"] = [d.metadata.get("source", "Internal KB") for d in state["kb_docs"]]
    return state

def generate_web_answer(state: AgentState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template("Answer using web results:\n{w}\n\nQuestion: {q}")
    res = llm.invoke(prompt.format_messages(w=state["web_results"], q=state["question"]))
    state["answer"] = get_text(res)
    state["citations"] = ["Tavily Web Search"]
    return state

def direct_answer(state: AgentState):
    llm = get_llm()
    res = llm.invoke(state["question"])
    state["answer"] = get_text(res)
    state["citations"] = ["Direct LLM"]
    return state

def insufficient_answer(state: AgentState):
    state["answer"] = "Could not find reliable evidence to resolve your IT ticket. Please contact the help desk."
    state["citations"] = ["None"]
    return state

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("route_question", route_question)
workflow.add_node("retrieve_kb", retrieve_kb)
workflow.add_node("grade_kb", grade_kb_evidence)
workflow.add_node("web_search", web_search)
workflow.add_node("grade_web", grade_web_evidence)
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("gen_kb", generate_kb_answer)
workflow.add_node("gen_web", generate_web_answer)
workflow.add_node("direct", direct_answer)
workflow.add_node("insufficient", insufficient_answer)

workflow.add_edge(START, "route_question")
workflow.add_conditional_edges("route_question", lambda s: "retrieve_kb" if s["source_used"] == "kb" else "direct")
workflow.add_edge("retrieve_kb", "grade_kb")
workflow.add_conditional_edges("grade_kb", lambda s: "gen_kb" if s["kb_grade"] == "good" else "web_search")
workflow.add_edge("web_search", "grade_web")
workflow.add_conditional_edges("grade_web", lambda s: "gen_web" if s["web_grade"] == "good" else ("rewrite_query" if s["retry_count"] < settings.max_retries else "insufficient"))
workflow.add_edge("rewrite_query", "web_search")

workflow.add_edge("gen_kb", END)
workflow.add_edge("gen_web", END)
workflow.add_edge("direct", END)
workflow.add_edge("insufficient", END)

app_graph = workflow.compile()

def ask(query: str):
    initial_state = {
        "question": query,
        "current_query": query,
        "kb_docs": [],
        "web_results": "",
        "kb_grade": "",
        "web_grade": "",
        "answer": "",
        "source_used": "",
        "retry_count": 0,
        "trace": [],
        "citations": []
    }
    return app_graph.invoke(initial_state)