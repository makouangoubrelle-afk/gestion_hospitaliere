# SGHL — Système de Gestion Hospitalière et de Laboratoire

Projet conforme au cahier des charges GI3 2025-2026.

## Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python 3, Django 5, Django Ninja |
| Frontend Web | Vue.js 3, Tailwind CSS, Axios |
| Mobile | Flutter (iOS / Android) |
| Base de données | PostgreSQL (SQLite en dev) |
| Auth | JWT (SimpleJWT) + rotation refresh tokens |
| API | `/api/v1/` versionnée |

## Modules fonctionnels

- **Gestion clinique** : consultations, diagnostic CIM-10, prescriptions électroniques
- **Hospitalisation** : Bâtiment → Service → Chambre → Lit (1 lit = 1 patient)
- **Laboratoire (LIS)** : Commande → Prélèvement → Saisie → Validation biologiste → Publication
- **Pharmacie** : stocks, lots, péremption, alertes rupture
- **Facturation** : factures, tiers payant, paiements partiels
- **RBAC** : rôles Admin, Médecin, Infirmier, Biologiste, Pharmacien, Comptable, Patient
- **Audit trail** : livre-journal immuable (user, timestamp, IP, old/new values)
- **Dashboard** : KPIs temps réel (occupation, recettes, examens en attente)
- **Mobile patient** : historique, rendez-vous, observance

## Données de démonstration (soutenance)

```bash
python manage.py seed_demo
```

Comptes créés automatiquement :

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| admin | Admin123! | Administrateur |
| medecin | Medecin123! | Médecin |
| biologiste | Bio123! | Biologiste |
| patient | Patient123! | Patient |

## Génération PDF

- **Factures** : `/factures/<id>/pdf/` (web) ou `/api/v1/factures/<id>/pdf` (API JWT)
- **Rapports labo** : `/laboratoire/<id>/pdf/` (web) ou `/api/v1/laboratoire/commandes/<id>/rapport-pdf` (API)
- **Publication LIS** : `POST /api/v1/laboratoire/commandes/<id>/publier` (après validation biologiste)

## Déploiement rapide

**Windows (local) :**
```powershell
cd toto
.\scripts\deploy.ps1
python manage.py runserver
```

**Docker (PostgreSQL + backend + frontend) :**
```bash
cd toto
docker compose up -d
# ou
bash scripts/deploy.sh
```

## CI/CD

Pipeline GitHub Actions (`.github/workflows/ci.yml`) :
- Tests backend pytest
- Build frontend Vue.js

## Installation backend

```bash
cd toto
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API Swagger : http://127.0.0.1:8000/api/v1/docs  
Endpoint santé : http://127.0.0.1:8000/api/v1/sante/

## Frontend Vue.js

```bash
cd frontend
npm install
npm run dev
```

Interface : http://localhost:5173

## Application mobile Flutter

```bash
cd mobile
flutter pub get
flutter run
```

## Tests

```bash
cd toto
pytest
```

## PostgreSQL (production)

Dans `.env` :

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=sghl
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

## Rôles RBAC

Assigner le rôle dans l'admin Django (`UserProfile`) :
- `admin`, `medecin`, `infirmier`, `biologiste`, `pharmacien`, `comptable`, `patient`

## Conformité cahier des charges

| Exigence | Statut |
|----------|--------|
| API REST Django Ninja `/api/v1/` | ✅ |
| JWT + rotation refresh | ✅ |
| Pagination API | ✅ |
| Endpoint `/sante/` | ✅ |
| Audit trail | ✅ |
| RBAC par profil | ✅ |
| Hospitalisation hiérarchique | ✅ |
| Workflow LIS | ✅ |
| Pharmacie + stocks | ✅ |
| Dashboard KPIs | ✅ |
| Vue.js 3 + Tailwind | ✅ |
| Flutter mobile patient | ✅ |
| PostgreSQL configurable | ✅ |
| Rate limiting | ✅ |
| Tests pytest | ✅ |
| Données de démo | ✅ |
| PDF factures & labo | ✅ |
| CI/CD GitHub Actions | ✅ |
| Docker / déploiement | ✅ |
