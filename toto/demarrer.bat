@echo off
cd /d "%~dp0"
title SGHL - Gestion Hospitaliere
echo.
echo ========================================
echo   SGHL - Demarrage du projet
echo ========================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo [1/6] Creation de l'environnement virtuel...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo [2/6] Migration de la base de donnees...
python manage.py migrate

echo [3/6] Compilation des langues...
python manage.py compile_i18n

echo [4/6] Comptes de connexion...
python manage.py ensure_users

echo [5/6] Chargement des donnees de demo...
python manage.py seed_demo

echo [6/6] Demarrage du serveur...
echo.
echo   Ouvrez votre navigateur sur :
echo   http://127.0.0.1:8000
echo.
echo   Connexion : admin / Admin123!
echo.
echo   NE FERMEZ PAS cette fenetre tant que vous utilisez l'application.
echo   Appuyez sur Ctrl+C pour arreter le serveur.
echo.

start "" "http://127.0.0.1:8000/login/"
python manage.py runserver 127.0.0.1:8000
