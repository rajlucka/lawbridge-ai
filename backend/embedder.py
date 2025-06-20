from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a lightweight model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, max_length=500):
    """
    Splits the raw legal text into smaller chunks (clauses or paragraphs)
    """
    chunks = []
    current_chunk = ""
    for line in text.split('\n'):
        if len(current_chunk) + len(line) < max_length:
            current_chunk += line + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def embed_chunks(chunks):
    """
    Converts a list of text chunks into embeddings
    """
    return model.encode(chunks)

def build_faiss_index(embeddings):
    """
    Builds a FAISS index for fast similarity search
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

def prepare_document_index(raw_text):
    """
    End-to-end: chunk, embed, and index a document
    Returns: index, chunks
    """
    chunks = chunk_text(raw_text)
    embeddings = embed_chunks(chunks)
    index = build_faiss_index(np.array(embeddings))
    return index, chunks