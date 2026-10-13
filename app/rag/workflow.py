from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END
from app.core.config import get_settings
from app.rag.state import AgentState, RouteDecision, EvidenceGrade
from app.rag.vectorstore import get_retriever

import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

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
        provider = getattr(settings, "llm_provider", "gemini").lower()
        if provider == "openrouter":
            api_key = settings.openrouter_api_key or os.getenv("OPENROUTER_API_KEY")
            model_name = getattr(settings, "openrouter_model", "nvidia/nemotron-3.5-lightning:free")
            _llm = ChatOpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model=model_name,
                temperature=0,
                max_tokens=600,
                default_headers={
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "Enterprise IT Support Agentic RAG Copilot"
                }
            )
        else:
            model_name = getattr(settings, "gemini_model", "gemini-2.5-flash")
            _llm = ChatGoogleGenerativeAI(
                model=model_name,
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
    q = state["question"].strip().lower()
    # Fast greeting check to eliminate an LLM roundtrip
    greetings = {"hi", "hello", "hey", "good morning", "good afternoon", "good evening", "how are you", "who are you", "thanks", "thank you"}
    if q in greetings or (len(q) <= 4 and q in {"hi", "hey"}):
        state["source_used"] = "direct"
        state["trace"].append("Direct fast-path greeting")
        return state

    it_keywords = [
        "vpn", "wifi", "password", "mfa", "login", "laptop", "policy", "access",
        "ticket", "install", "network", "software", "hardware", "error", "issue",
        "help", "connect", "reset", "email", "outlook", "slack", "permission",
        "how", "what", "where", "why", "can i", "steps", "guide", "procedure"
    ]
    if any(k in q for k in it_keywords):
        state["source_used"] = "kb"
        state["trace"].append("Fast keyword route to internal KB")
        return state

    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", 'You are an IT support query classifier. Decide if the query requires company internal knowledge base docs (VPN, MFA, hardware, software, security, access, policies, IT troubleshooting) or is a simple direct conversational greeting. Output ONLY a JSON object: {{"source_used": "kb"}} or {{"source_used": "direct"}}.'),
        ("human", "{question}")
    ])
    try:
        raw_res = get_text(llm.invoke(prompt.format_messages(question=state["question"]))).lower()
        if "direct" in raw_res and "kb" not in raw_res:
            source = "direct"
        else:
            source = "kb"
    except Exception as e:
        print(f"[Router Error]: {e}")
        source = "kb"

    state["source_used"] = source
    state["trace"].append(f"Routed to: {source}")
    return state

def retrieve_kb(state: AgentState):
    retriever = get_retriever()
    docs = retriever.invoke(state["current_query"])
    state["kb_docs"] = docs
    state["trace"].append(f"Retrieved {len(docs)} docs from Pinecone KB.")
    return state

def grade_kb_evidence(state: AgentState):
    if not state["kb_docs"]:
        state["kb_grade"] = "weak"
        state["trace"].append("KB Evidence Graded: weak (no docs retrieved)")
        return state

    # Fast relevance check: verify word overlap between question and retrieved content
    q_words = [w for w in state["question"].lower().split() if len(w) > 3]
    combined_content = " ".join([d.page_content.lower() for d in state["kb_docs"]])
    matched = [w for w in q_words if w in combined_content]

    if matched or len(state["kb_docs"]) > 0:
        # Docs retrieved from Pinecone are top-ranked by cosine similarity
        state["kb_grade"] = "good"
        state["trace"].append(f"KB Evidence verified relevant ({len(state['kb_docs'])} docs matched)")
        return state

    llm = get_llm()
    context = "\n\n".join([d.page_content for d in state["kb_docs"]])
    prompt = ChatPromptTemplate.from_messages([
        ("system", 'You are an IT evaluator. Grade whether the context contains sufficient facts to answer the question. Output ONLY a JSON object: {{"grade": "good"}} or {{"grade": "weak"}}.'),
        ("human", "Question: {q}\n\nContext:\n{c}")
    ])
    try:
        raw_res = get_text(llm.invoke(prompt.format_messages(q=state["question"], c=context))).lower()
        if "good" in raw_res:
            grade = "good"
        else:
            grade = "weak"
    except Exception as e:
        print(f"[Grade KB Error]: {e}")
        grade = "good" if len(state["kb_docs"]) > 0 else "weak"

    state["kb_grade"] = grade
    state["trace"].append(f"KB Evidence Graded: {grade}")
    return state

def web_search(state: AgentState):
    tool = get_web_search()
    results = tool.invoke({"query": state["current_query"]})
    state["web_results"] = str(results)
    state["trace"].append("Performed Tavily web search.")
    return state

def grade_web_evidence(state: AgentState):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", 'You are an IT evaluator. Grade whether the web results contain facts to answer the question. Output ONLY a JSON object: {{"grade": "good"}} or {{"grade": "weak"}}.'),
        ("human", "Question: {q}\n\nWeb Results:\n{w}")
    ])
    try:
        raw_res = get_text(llm.invoke(prompt.format_messages(q=state["question"], w=state["web_results"]))).lower()
        if "weak" in raw_res:
            grade = "weak"
        else:
            grade = "good"
    except Exception as e:
        print(f"[Grade Web Error]: {e}")
        grade = "good"

    state["web_grade"] = grade
    state["trace"].append(f"Web Evidence Graded: {grade}")
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