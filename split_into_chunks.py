from typing import List
from sentence_transformers import SentenceTransformer 
import chromadb

embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
chromadb_client = chromadb.EphemeralClient()
def split_into_chunks(doc: str) -> List[str]:
    with open("doc.md", "r", encoding='utf-8') as file:
        content = file.read()
        chunks = content.split("\n\n") 
        return chunks

chunks = split_into_chunks("doc.md")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")

def embed_chunks(chunks: List[str]) -> List[List[float]]:
    embedding = embedding_model.encode(chunks)
    return embedding

embeddings = embed_chunks(chunks)

for i, embeddings in enumerate(embeddings):
    print(f"Embedding for Chunk {i+1}:\n{embeddings}\n")