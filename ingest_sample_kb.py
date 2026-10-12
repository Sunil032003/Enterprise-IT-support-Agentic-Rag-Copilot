from app.services.ingestion import load_file,chunk_documents
from pathlib import Path
from app.rag.vectorstore import add_documents_to_vector_store
import os

all_docs=[]

for doc in Path("data/sample_kb").glob("*"):
    if doc.is_file():
        loaded_doc=load_file(doc)
        chunked_doc=chunk_documents(loaded_doc)
        all_docs.extend(chunked_doc)
print(f"Total documents to add: {len(loaded_doc)}")
print(len(chunked_doc))
add_documents_to_vector_store(all_docs)

