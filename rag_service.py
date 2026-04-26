from __future__ import annotations

from functools import lru_cache
from typing import Any

from embeddings import embed_query, embed_texts, load_embedding_model
from gemini_llm import DEFAULT_GEMINI_MODEL, generate_answer
from rerank import load_model, rerank
from split_into_chunks import split_into_chunks
from vector_store import create_chroma_collection, query_collection, store_embeddings

DOCUMENT_PATH = "doc.md"
EMBEDDING_MODEL_NAME = "shibing624/text2vec-base-chinese"


@lru_cache(maxsize=1)
def _build_index(
    document_path: str = DOCUMENT_PATH,
    embedding_model_name: str = EMBEDDING_MODEL_NAME,
) -> dict[str, Any]:
    chunks = split_into_chunks(document_path)
    embedding_model = load_embedding_model(embedding_model_name)
    embeddings = embed_texts(embedding_model, chunks)

    collection = create_chroma_collection()
    store_embeddings(collection, chunks, embeddings)

    return {
        "chunks": chunks,
        "embedding_model": embedding_model,
        "collection": collection,
    }


@lru_cache(maxsize=1)
def _get_rerank_model():
    return load_model()


def _normalize_query_results(results: dict[str, Any]) -> list[dict[str, Any]]:
    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    normalized: list[dict[str, Any]] = []
    for index, document in enumerate(documents):
        distance = distances[index] if index < len(distances) else None
        normalized.append(
            {
                "rank": index + 1,
                "id": ids[index] if index < len(ids) else f"chunk_{index}",
                "document": document,
                "distance": float(distance) if distance is not None else None,
            }
        )

    return normalized


def run_rag(
    query: str,
    n_results: int = 5,
    rerank_top_k: int = 3,
    document_path: str = DOCUMENT_PATH,
    embedding_model_name: str = EMBEDDING_MODEL_NAME,
    llm_model_name: str = DEFAULT_GEMINI_MODEL,
    use_llm: bool = True,
) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("Query must not be empty.")

    index = _build_index(document_path=document_path, embedding_model_name=embedding_model_name)
    query_embedding = embed_query(index["embedding_model"], query)
    results = query_collection(index["collection"], query_embedding, n_results=n_results)
    similar_results = _normalize_query_results(results)

    candidates = [item["document"] for item in similar_results]
    reranked_results: list[str] = []
    if candidates:
        rerank_model = _get_rerank_model()
        reranked_results = rerank(rerank_model, query, candidates, top_k=rerank_top_k)

    retrieval_result = reranked_results[0] if reranked_results else None
    generated_answer = None
    llm_status = "disabled"

    if use_llm and reranked_results:
        try:
            generated_answer = generate_answer(
                query=query,
                context_chunks=reranked_results,
                model_name=llm_model_name,
            )
            llm_status = "generated"
        except ValueError as exc:
            llm_status = str(exc)

    final_result = generated_answer or retrieval_result

    return {
        "query": query,
        "document_path": document_path,
        "embedding_model": embedding_model_name,
        "llm_model": llm_model_name,
        "llm_enabled": use_llm,
        "llm_status": llm_status,
        "chunk_count": len(index["chunks"]),
        "n_results": n_results,
        "rerank_top_k": rerank_top_k,
        "retrieval_result": retrieval_result,
        "generated_answer": generated_answer,
        "final_result": final_result,
        "similar_results": similar_results,
        "reranked_results": reranked_results,
    }
