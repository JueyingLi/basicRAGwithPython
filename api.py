from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from gemini_llm import DEFAULT_GEMINI_MODEL
from rag_service import DOCUMENT_PATH, EMBEDDING_MODEL_NAME, run_rag

app = FastAPI(title="Basic RAG API", version="0.1.0")


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Question to search for")
    n_results: int = Field(default=5, ge=1, le=20)
    rerank_top_k: int = Field(default=3, ge=1, le=20)
    document_path: str = Field(default=DOCUMENT_PATH)
    embedding_model_name: str = Field(default=EMBEDDING_MODEL_NAME)
    llm_model_name: str = Field(default=DEFAULT_GEMINI_MODEL)
    use_llm: bool = Field(default=True)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Basic RAG API is running.",
        "query_endpoint": "/query",
    }


@app.post("/query")
def query_rag(request: QueryRequest) -> dict:
    try:
        return run_rag(
            query=request.query,
            n_results=request.n_results,
            rerank_top_k=request.rerank_top_k,
            document_path=request.document_path,
            embedding_model_name=request.embedding_model_name,
            llm_model_name=request.llm_model_name,
            use_llm=request.use_llm,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
