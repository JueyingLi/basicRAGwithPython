#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif [[ -x "$ROOT_DIR/.venv/Scripts/python.exe" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/Scripts/python.exe"
else
  echo "Could not find a project Python executable in .venv." >&2
  exit 1
fi

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then
    kill "$API_PID" >/dev/null 2>&1 || true
  fi

  if [[ -n "${STREAMLIT_PID:-}" ]]; then
    kill "$STREAMLIT_PID" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

cd "$ROOT_DIR"

echo "Starting FastAPI on http://127.0.0.1:8000 ..."
"$PYTHON_BIN" -m uvicorn api:app --host 127.0.0.1 --port 8000 --reload &
API_PID=$!

echo "Starting Streamlit on http://127.0.0.1:8501 ..."
"$PYTHON_BIN" -m streamlit run streamlit_app.py --server.headless true &
STREAMLIT_PID=$!

echo
echo "Both services are starting:"
echo "FastAPI:   http://127.0.0.1:8000/docs"
echo "Streamlit: http://127.0.0.1:8501"
echo
echo "Press Ctrl+C to stop both."

wait "$API_PID" "$STREAMLIT_PID"
