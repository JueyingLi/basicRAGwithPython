from __future__ import annotations

import importlib.util
import subprocess
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
REQUIRED_MODULES = ("fastapi", "streamlit", "uvicorn")


def get_python_executable() -> str:
    if sys.executable:
        return sys.executable

    raise RuntimeError("Could not determine the current Python executable.")


def start_process(args: list[str]) -> subprocess.Popen:
    return subprocess.Popen(args, cwd=ROOT_DIR)


def find_missing_modules() -> list[str]:
    missing: list[str] = []
    for module_name in REQUIRED_MODULES:
        if importlib.util.find_spec(module_name) is None:
            missing.append(module_name)

    return missing


def stop_process(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return

    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main() -> int:
    python_executable = get_python_executable()
    missing_modules = find_missing_modules()

    if missing_modules:
        print("Missing required packages:", ", ".join(missing_modules))
        print("Install them with:")
        print(f'"{python_executable}" -m pip install -r requirements.txt')
        return 1

    print("Starting FastAPI on http://127.0.0.1:8000 ...")
    api_process = start_process(
        [
            python_executable,
            "-m",
            "uvicorn",
            "api:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--reload",
        ]
    )

    print("Starting Streamlit on http://127.0.0.1:8501 ...")
    streamlit_process = start_process(
        [
            python_executable,
            "-m",
            "streamlit",
            "run",
            "streamlit_app.py",
            "--server.headless",
            "true",
        ]
    )

    print()
    print("Both services are starting:")
    print("FastAPI:   http://127.0.0.1:8000/docs")
    print("Streamlit: http://127.0.0.1:8501")
    print()
    print("Press Ctrl+C to stop both.")

    try:
        while True:
            api_code = api_process.poll()
            streamlit_code = streamlit_process.poll()

            if api_code is not None:
                print(f"FastAPI exited with code {api_code}.")
                return api_code

            if streamlit_code is not None:
                print(f"Streamlit exited with code {streamlit_code}.")
                return streamlit_code

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")
        return 0
    finally:
        stop_process(api_process)
        stop_process(streamlit_process)


if __name__ == "__main__":
    raise SystemExit(main())
