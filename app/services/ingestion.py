from pathlib import Path
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader,Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_file(file_path):
    file_path = Path(file_path)

    if file_path.suffix == ".pdf":
        return PyPDFLoader(str(file_path)).load()

    elif file_path.suffix in [".txt", ".md"]:
        return TextLoader(str(file_path), encoding="utf-8").load()

    elif file_path.suffix == ".docx":
        return Docx2txtLoader(str(file_path)).load()

    else:
        raise ValueError("Unsupported file type")


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120
    )

    return splitter.split_documents(documents)