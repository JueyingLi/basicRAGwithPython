from typing import List


def load_document(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def split_into_chunks(file_path: str) -> List[str]:
    content = load_document(file_path)
    return [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
