from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from app.core.config import get_settings


_vector_store = None
_retriever = None

def get_vector_store():
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    settings = get_settings()

    # 1. Create embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model=settings.embedding_model,
        google_api_key=settings.gemini_api_key
    )

    # 2. Connect to Pinecone
    pc = Pinecone(
        api_key=settings.pinecone_api_key
    )

    # 3. Create index if it doesn't exist
    if not pc.has_index(settings.pinecone_index_name):
        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    # 4. Get Pinecone index
    index = pc.Index(
        settings.pinecone_index_name
    )

    # 5. Create vector store
    _vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace=settings.pinecone_namespace
    )

    return _vector_store

def add_documents_to_vector_store(documents):

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    return vector_store

# Alias for router compatibility
add_documents = add_documents_to_vector_store


def get_retriever():
    global _retriever
    if _retriever is not None:
        return _retriever

    # Get vector store
    vector_store = get_vector_store()

    # Create retriever
    _retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return _retriever

