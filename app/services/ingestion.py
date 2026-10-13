from pathlib import Path
import pypdf
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf_safely(file_path: Path):
    """
    Safely loads PDF documents with multi-stage recovery:
    1. Standard PyPDFLoader
    2. Detection of text/markdown files renamed with .pdf extension
    3. Permissive page-by-page extraction (ignoring corrupted stream objects)
    """
    # 1. Standard PyPDFLoader attempt
    try:
        docs = PyPDFLoader(str(file_path)).load()
        if docs and any(d.page_content.strip() for d in docs):
            return docs
    except Exception as e:
        print(f"[PDF Loader] Standard PyPDFLoader failed on {file_path.name} ({e}). Attempting recovery...")

    # 2. Check if file is actually a plain text / Markdown file named as .pdf
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.strip():
            print(f"[PDF Loader] Successfully recovered {file_path.name} as text document.")
            return [Document(page_content=content, metadata={"source": file_path.name})]
    except UnicodeDecodeError:
        pass
    except Exception:
        pass

    # 3. Permissive page-by-page extraction
    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f, strict=False)
            extracted_docs = []
            for i, page in enumerate(reader.pages):
                try:
                    text = page.extract_text()
                    if text and text.strip():
                        extracted_docs.append(Document(
                            page_content=text,
                            metadata={"source": file_path.name, "page": i + 1}
                        ))
                except Exception as page_err:
                    print(f"[PDF Loader] Skipped corrupt stream on page {i+1}: {page_err}")

            if extracted_docs:
                return extracted_docs
    except Exception as pdf_err:
        print(f"[PDF Loader] Permissive extraction failed: {pdf_err}")

    raise ValueError(
        f"Unable to read {file_path.name}. The file appears to be corrupted or is not a valid PDF document."
    )


def load_file(file_path):
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return load_pdf_safely(file_path)

    elif suffix in [".txt", ".md"]:
        return TextLoader(str(file_path), encoding="utf-8").load()

    elif suffix == ".docx":
        return Docx2txtLoader(str(file_path)).load()

    else:
        raise ValueError(f"Unsupported file type: {file_path.suffix}")


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120
    )

    return splitter.split_documents(documents)