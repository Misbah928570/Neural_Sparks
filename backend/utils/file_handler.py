from werkzeug.datastructures import FileStorage
from pdfminer.high_level import extract_text as pdf_extract
from docx import Document
import io

def read_any_file(f: FileStorage) -> str:
    """
    Reads PDF, DOCX, or TXT files and returns text content.
    """
    name = (f.filename or "").lower()
    b = f.read()

    if name.endswith(".pdf"):  # FIXED TYPO HERE
        with io.BytesIO(b) as fh:
            return pdf_extract(fh)

    elif name.endswith(".docx"):  # FIXED TYPO HERE
        with io.BytesIO(b) as fh:
            doc = Document(fh)
            return "\n".join(p.text for p in doc.paragraphs)

    # default txt/others
    try:
        return b.decode("utf-8", errors="ignore")
    except Exception:
        return ""
