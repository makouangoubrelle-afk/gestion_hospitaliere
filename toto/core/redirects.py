from django.urls import reverse

from accounts.models import Role

# Anciennes URL ou alias → page canonique (nom d'URL Django)
LEGACY_URL_REDIRECTS = {
    '/urgences': 'salles_urgence',
    '/urgences/': 'salles_urgence',
    '/attente': 'salles_attente',
    '/attente/': 'salles_attente',
    '/rdv': 'agenda',
    '/rdv/': 'agenda',
    '/rendez-vous': 'agenda',
    '/rendez-vous/': 'agenda',
    '/rendezvous': 'agenda',
    '/rendezvous/': 'agenda',
    '/facturation': 'factures',
    '/facturation/': 'factures',
    '/facture': 'factures',
    '/facture/': 'factures',
    '/paiements': 'paiement',
    '/paiements/': 'paiement',
    '/accueil': 'home',
    '/accueil/': 'home',
}

# Page d'accueil par rôle après connexion (si pas de ?next=)
ROLE_HOME_URL_NAMES = {
    Role.ADMIN: 'dashboard',
    Role.MEDECIN: 'consultations',
    Role.INFIRMIER: 'infirmiers',
    Role.SECRETAIRE: 'secretaires',
    Role.BIOLOGISTE: 'laboratoire',
    Role.PHARMACIEN: 'pharmacie',
    Role.COMPTABLE: 'factures',
    Role.PATIENT: 'home',
}


def get_role_home_url(user):
    profile = getattr(user, 'profile', None)
    if not profile:
        return reverse('home')
    url_name = ROLE_HOME_URL_NAMES.get(profile.role, 'home')
    return reverse(url_name)


def resolve_legacy_redirect(path):
    """Retourne le nom d'URL canonique si path est un alias, sinon None."""
    if path in LEGACY_URL_REDIRECTS:
        return LEGACY_URL_REDIRECTS[path]
    if path != '/' and path.endswith('/'):
        trimmed = path.rstrip('/')
        if trimmed in LEGACY_URL_REDIRECTS:
            return LEGACY_URL_REDIRECTS[trimmed]
    return None
