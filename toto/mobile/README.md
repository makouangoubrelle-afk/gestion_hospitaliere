# SGHL — Application mobile patient

## Lien web (recommandé)

Avec le serveur Django lancé :

**http://127.0.0.1:8000/mobile/**

Sur Render (après déploiement) :

**https://sg-hospitaliere.onrender.com/mobile/**

Compte démo : `patient` / `patient1234`

## Lancer en local (émulateur / téléphone)

```bash
cd toto
python manage.py runserver
```

Dans un autre terminal :

```bash
cd toto/mobile
flutter pub get
flutter run
```

## Rebuild web (après modification Flutter)

```bash
cd toto/mobile
flutter build web --release --base-href /mobile/ --output ../mobile_dist
```

Puis redémarrer Django. Le dossier `mobile_dist/` est servi sous `/mobile/`.
