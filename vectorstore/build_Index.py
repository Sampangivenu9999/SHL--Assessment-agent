import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load JSON data
with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create text list
texts = []

for item in assessments:
    text = item["name"]
    texts.append(text)

# Create embeddings
embeddings = model.encode(texts)

# Convert to numpy array
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

# Save index
faiss.write_index(index, "vectorstore/faiss_index.bin")

print("FAISS index created successfully!")
print("Total embeddings:", len(texts))