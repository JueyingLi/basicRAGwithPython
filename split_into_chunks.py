from typing import List
from sentence_transformers import SentenceTransformer 
import chromadb

embedding_model = SentenceTransformer("shibing624/text2vec-base-chinese")
chromadb_client = chromadb.EphemeralClient()
chromadb_collection = chromadb_client.create_collection(name="my_collection")  

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

def store_embeddings(chunks: List[str], embeddings: List[List[float]]):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        chromadb_collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=[embedding]
        )

store_embeddings(chunks, embeddings)

