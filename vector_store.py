from typing import Any, Dict, List

import chromadb


def create_chroma_collection(collection_name: str = "my_collection") -> Any:
    client = chromadb.EphemeralClient()
    return client.create_collection(name=collection_name)


def store_embeddings(
    collection: Any,
    chunks: List[str],
    embeddings: List[List[float]],
) -> None:
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=[embedding],
        )


def query_collection(
    collection: Any,
    query_embedding: List[float],
    n_results: int = 5,
) -> Dict[str, Any]:
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
