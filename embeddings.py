from typing import List

from sentence_transformers import SentenceTransformer


def load_embedding_model(model_name: str) -> SentenceTransformer:
    return SentenceTransformer(model_name)


def embed_texts(model: SentenceTransformer, texts: List[str]) -> List[List[float]]:
    embeddings = model.encode(texts)
    return embeddings.tolist()


def embed_query(model: SentenceTransformer, query: str) -> List[float]:
    embedding = model.encode([query])[0]
    return embedding.tolist()
