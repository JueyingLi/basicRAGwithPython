from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

DEFAULT_GEMINI_MODEL = "gemini-2.5-pro"

SYSTEM_INSTRUCTION = (
    "You are a helpful RAG assistant. Answer the user's question using only the "
    "provided context. If the context is insufficient, say so clearly. Keep the "
    "answer grounded in the retrieved text and do not invent facts."
)


def _load_environment() -> None:
    load_dotenv()


def get_api_key() -> str | None:
    _load_environment()
    return os.getenv("GEMINI_API_KEY")


@lru_cache(maxsize=2)
def get_client(api_key: str):
    return genai.Client(api_key=api_key)


def build_prompt(query: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(
        f"Context {index + 1}:\n{chunk}" for index, chunk in enumerate(context_chunks)
    )
    return (
        f"Question:\n{query}\n\n"
        f"Retrieved context:\n{context}\n\n"
        "Answer the question based on the retrieved context."
    )


def generate_answer(
    query: str,
    context_chunks: list[str],
    model_name: str = DEFAULT_GEMINI_MODEL,
) -> str:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set.")

    if not context_chunks:
        raise ValueError("No context chunks were provided for generation.")

    client = get_client(api_key)
    prompt = build_prompt(query, context_chunks)
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
        ),
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text.strip()
