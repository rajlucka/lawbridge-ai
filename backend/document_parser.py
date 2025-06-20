import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file):
    """
    Extracts and returns text from a PDF file using PyMuPDF.
    """
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

def extract_text_from_docx(file):
    """
    Extracts and returns text from a DOCX file using python-docx.
    """
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def parse_document(uploaded_file):
    """
    Determines file type and parses document text accordingly.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
