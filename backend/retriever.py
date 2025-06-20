from sentence_transformers import SentenceTransformer
import numpy as np

# Load the same model as used for chunk embedding
model = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_relevant_chunks(user_query, faiss_index, chunks, top_k=3):
    """
    Retrieves the top-k most relevant text chunks from the document
    based on semantic similarity with the user's query.
    """
    query_embedding = model.encode([user_query])
    distances, indices = faiss_index.search(np.array(query_embedding), top_k)
    
    results = []
    for idx in indices[0]:
        results.append(chunks[idx])
    return results
