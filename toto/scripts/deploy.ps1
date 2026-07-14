# Script de déploiement SGHL (Windows PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "=== Deploiement SGHL ===" -ForegroundColor Cyan

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Fichier .env cree — modifiez-le avant la production."
}

Write-Host ">> Installation des dependances Python..."
pip install -r requirements.txt

Write-Host ">> Migrations..."
python manage.py migrate

Write-Host ">> Donnees de demonstration..."
python manage.py seed_demo

Write-Host ">> Verification..."
python manage.py check
pytest core/tests_api.py -q

Write-Host ""
Write-Host "=== SGHL pret ===" -ForegroundColor Green
Write-Host "  Demarrer : python manage.py runserver"
Write-Host "  API docs : http://127.0.0.1:8000/api/v1/docs"
Write-Host ""
Write-Host "Comptes demo :"
Write-Host "  admin / Admin123!"
Write-Host "  medecin / Medecin123!"
Write-Host "  biologiste / Bio123!"
Write-Host "  patient / Patient123!"
