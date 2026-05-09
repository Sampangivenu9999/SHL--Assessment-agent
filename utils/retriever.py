import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("vectorstore/faiss_index.bin")

# Load assessment data
with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

def search_assessments(query, top_k=5):

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(assessments[idx])

    return results