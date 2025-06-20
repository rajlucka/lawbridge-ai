import re

def clean_text(text):
    """
    Remove excessive whitespace and non-printable characters
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def count_tokens(text, tokenizer=None):
    """
    Rough token count using whitespace or OpenAI tokenizer if passed
    """
    if tokenizer:
        return len(tokenizer.encode(text))
    return len(text.split())

def is_allowed_file(filename):
    """
    Check if file is PDF or DOCX
    """
    return filename.endswith(".pdf") or filename.endswith(".docx")
