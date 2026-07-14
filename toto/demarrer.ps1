# SGHL - Demarrage rapide (PowerShell)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "=== Demarrage SGHL ===" -ForegroundColor Cyan

if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "Creation du venv..."
    python -m venv venv
    & .\venv\Scripts\pip.exe install -r requirements.txt
}

& .\venv\Scripts\python.exe manage.py migrate
& .\venv\Scripts\python.exe manage.py seed_demo

Write-Host ""
Write-Host "Backend : http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Login   : admin / Admin123!" -ForegroundColor Green
Write-Host ""

& .\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
