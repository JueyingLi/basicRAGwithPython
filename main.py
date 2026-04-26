import sys

from gemini_llm import DEFAULT_GEMINI_MODEL
from rag_service import DOCUMENT_PATH, EMBEDDING_MODEL_NAME, run_rag

QUERY = "哆啦A梦的三个秘密道具是什么？"


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def print_results(response: dict) -> None:
    print(f"Query: {response['query']}")
    print(f"Document: {response['document_path']}")
    print(f"Total chunks: {response['chunk_count']}")
    print(f"LLM model: {response['llm_model']}")
    print(f"LLM status: {response['llm_status']}")

    print("\nTop similar results:")
    for item in response["similar_results"]:
        print(f"Rank {item['rank']} | Distance: {item['distance']}")
        print(item["document"])
        print()

    print("Reranked results:")
    for i, result in enumerate(response["reranked_results"], start=1):
        print(f"Rank {i}: {result}")

    print("\nTop retrieval result:")
    print(response["retrieval_result"])

    print("\nFinal result:")
    print(response["final_result"])


def main() -> None:
    configure_stdout()
    response = run_rag(
        query=QUERY,
        document_path=DOCUMENT_PATH,
        embedding_model_name=EMBEDDING_MODEL_NAME,
        llm_model_name=DEFAULT_GEMINI_MODEL,
    )
    print_results(response)


if __name__ == "__main__":
    main()
