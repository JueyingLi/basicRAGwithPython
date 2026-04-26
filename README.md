# basicRAGwithPython

A small RAG demo that chunks a Markdown document, embeds each chunk, stores the
vectors in ChromaDB, reranks the best chunks, and can use Gemini 2.5 Pro to
generate a final grounded answer.

## Files

- `main.py`: runs the full demo pipeline.
- `split_into_chunks.py`: loads `doc.md` and splits it into text chunks.
- `embeddings.py`: loads the SentenceTransformer model and creates embeddings.
- `vector_store.py`: creates the ChromaDB collection, stores vectors, and queries it.
- `similarity.py`: shared vector math helpers, starting with cosine similarity.
- `gemini_llm.py`: calls Gemini to turn retrieved chunks into a final answer.

## Gemini Setup

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

If `GEMINI_API_KEY` is not set, the app will fall back to the top reranked chunk.

## Run

```powershell
uv run python main.py
```

## FastAPI

```powershell
uv run uvicorn api:app --reload
```

Then open `http://127.0.0.1:8000/docs` to test the API.

## Streamlit

```powershell
uv run streamlit run streamlit_app.py
```

## Run Both

PowerShell:

```powershell
.\run_local.ps1
```

Shell:

```bash
./run_local.sh
```

This starts FastAPI and Streamlit together and stops both when you exit.

Python:

```powershell
python run_local.py
```

If you are using the virtual environment directly:

```powershell
.\.venv\Scripts\python.exe run_local.py
```
