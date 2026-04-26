$ErrorActionPreference = "Stop"

function Get-PythonPath {
    $windowsPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
    if (Test-Path $windowsPython) {
        return $windowsPython
    }

    $unixPython = Join-Path $PSScriptRoot ".venv\bin\python"
    if (Test-Path $unixPython) {
        return $unixPython
    }

    throw "Could not find a project Python executable in .venv."
}

$pythonPath = Get-PythonPath

Write-Host "Starting FastAPI on http://127.0.0.1:8000 ..."
$apiProcess = Start-Process -FilePath $pythonPath `
    -ArgumentList "-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000", "--reload" `
    -WorkingDirectory $PSScriptRoot `
    -PassThru

Write-Host "Starting Streamlit on http://127.0.0.1:8501 ..."
$streamlitProcess = Start-Process -FilePath $pythonPath `
    -ArgumentList "-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true" `
    -WorkingDirectory $PSScriptRoot `
    -PassThru

Write-Host ""
Write-Host "Both services are starting:"
Write-Host "FastAPI:   http://127.0.0.1:8000/docs"
Write-Host "Streamlit: http://127.0.0.1:8501"
Write-Host ""
Write-Host "Press Ctrl+C to stop both."

try {
    while (-not $apiProcess.HasExited -and -not $streamlitProcess.HasExited) {
        Start-Sleep -Seconds 2
        $apiProcess.Refresh()
        $streamlitProcess.Refresh()
    }
}
finally {
    if (-not $apiProcess.HasExited) {
        Stop-Process -Id $apiProcess.Id
    }

    if (-not $streamlitProcess.HasExited) {
        Stop-Process -Id $streamlitProcess.Id
    }
}
