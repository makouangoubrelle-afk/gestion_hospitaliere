#!/usr/bin/env bash
set -euo pipefail

echo "=== Déploiement SGHL ==="

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Fichier .env créé — modifiez-le avant la production."
fi

echo ">> Construction Docker..."
docker compose build

echo ">> Démarrage des services..."
docker compose up -d db web

echo ">> Attente PostgreSQL..."
sleep 5

echo ">> Migrations et données de démo..."
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_demo

echo ""
echo "=== SGHL déployé avec succès ==="
echo "  Backend  : http://localhost:8000"
echo "  API docs : http://localhost:8000/api/v1/docs"
echo "  Santé    : http://localhost:8000/api/v1/sante/"
echo ""
echo "Comptes démo : admin/Admin123! | medecin/Medecin123! | biologiste/Bio123! | patient/Patient123!"
echo ""
echo "Frontend Vue (optionnel) : docker compose up -d frontend"
