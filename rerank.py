from typing import List
from sentence_transformers import CrossEncoder

def load_model() -> CrossEncoder:
    return CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(model: CrossEncoder, query: str, candidates: List[str], top_k: int = 3) -> List[str]:
    pairs = [(query, candidate) for candidate in candidates]
    scores = model.predict(pairs)
    return [candidate for _, candidate in sorted(zip(scores, candidates), reverse=True)][:top_k]