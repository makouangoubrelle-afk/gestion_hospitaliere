"""
URL configuration for SGHL project.
"""
from urllib.parse import quote

from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.views.generic import RedirectView

from core.ninja_api import api
from core import crud_views
from core import payment_views
from core.views import (
    home,
    user_login,
    register,
    patients_list,
    medecins_list,
    infirmiers_list,
    geolocalisation_list,
    secretaires_list,
    salles_urgence_list,
    salles_attente_list,
    agenda_list,
    consultations_list,
    invoices_list,
    payments_list,
    services_list,
    dashboard,
    hospitalisation_list,
    laboratoire_list,
    pharmacie_list,
    invoice_pdf,
    labo_pdf,
)

_original_admin_login = admin.site.login


def admin_login_redirect(request, extra_context=None):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return _original_admin_login(request, extra_context)
        messages.error(request, 'Accès réservé aux administrateurs.')
        return redirect('home')
    return redirect(f'/login/?next={quote(request.get_full_path())}')


admin.site.login = admin_login_redirect

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('api/v1/', api.urls),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('patients/', patients_list, name='patients'),
    path('patients/ajouter/', crud_views.patient_create, name='patient_create'),
    path('patients/<int:pk>/modifier/', crud_views.patient_update, name='patient_update'),
    path('patients/<int:pk>/supprimer/', crud_views.patient_delete, name='patient_delete'),
    path('medecins/', medecins_list, name='medecins'),
    path('medecins/ajouter/', crud_views.medecin_create, name='medecin_create'),
    path('medecins/<int:pk>/modifier/', crud_views.medecin_update, name='medecin_update'),
    path('medecins/<int:pk>/supprimer/', crud_views.medecin_delete, name='medecin_delete'),
    path('infirmiers/', infirmiers_list, name='infirmiers'),
    path('infirmiers/ajouter/', crud_views.infirmier_create, name='infirmier_create'),
    path('infirmiers/<int:pk>/modifier/', crud_views.infirmier_update, name='infirmier_update'),
    path('infirmiers/<int:pk>/supprimer/', crud_views.infirmier_delete, name='infirmier_delete'),
    path('geolocalisation/', geolocalisation_list, name='geolocalisation'),
    path('geolocalisation/ajouter/', crud_views.site_create, name='site_create'),
    path('geolocalisation/<int:pk>/modifier/', crud_views.site_update, name='site_update'),
    path('geolocalisation/<int:pk>/supprimer/', crud_views.site_delete, name='site_delete'),
    path('secretaires/', secretaires_list, name='secretaires'),
    path('secretaires/ajouter/', crud_views.secretaire_create, name='secretaire_create'),
    path('secretaires/<int:pk>/modifier/', crud_views.secretaire_update, name='secretaire_update'),
    path('secretaires/<int:pk>/supprimer/', crud_views.secretaire_delete, name='secretaire_delete'),
    path('salles-urgence/', salles_urgence_list, name='salles_urgence'),
    path('urgences/', RedirectView.as_view(pattern_name='salles_urgence', permanent=False)),
    path('salles-urgence/ajouter/', crud_views.salle_urgence_create, name='salle_urgence_create'),
    path('salles-urgence/<int:pk>/modifier/', crud_views.salle_urgence_update, name='salle_urgence_update'),
    path('salles-urgence/<int:pk>/supprimer/', crud_views.salle_urgence_delete, name='salle_urgence_delete'),
    path('salles-attente/', salles_attente_list, name='salles_attente'),
    path('attente/', RedirectView.as_view(pattern_name='salles_attente', permanent=False)),
    path('salles-attente/ajouter/', crud_views.salle_attente_create, name='salle_attente_create'),
    path('salles-attente/<int:pk>/modifier/', crud_views.salle_attente_update, name='salle_attente_update'),
    path('salles-attente/<int:pk>/supprimer/', crud_views.salle_attente_delete, name='salle_attente_delete'),
    path('salles-attente/file/ajouter/', crud_views.file_attente_create, name='file_attente_create'),
    path('salles-attente/file/<int:pk>/modifier/', crud_views.file_attente_update, name='file_attente_update'),
    path('salles-attente/file/<int:pk>/supprimer/', crud_views.file_attente_delete, name='file_attente_delete'),
    path('agenda/', agenda_list, name='agenda'),
    path('rdv/', RedirectView.as_view(pattern_name='agenda', permanent=False)),
    path('rendez-vous/', RedirectView.as_view(pattern_name='agenda', permanent=False)),
    path('rendezvous/', RedirectView.as_view(pattern_name='agenda', permanent=False)),
    path('agenda/ajouter/', crud_views.rendez_vous_create, name='rendez_vous_create'),
    path('agenda/<int:pk>/modifier/', crud_views.rendez_vous_update, name='rendez_vous_update'),
    path('agenda/<int:pk>/supprimer/', crud_views.rendez_vous_delete, name='rendez_vous_delete'),
    path('consultations/', consultations_list, name='consultations'),
    path('consultations/ajouter/', crud_views.consultation_create, name='consultation_create'),
    path('consultations/<int:pk>/modifier/', crud_views.consultation_update, name='consultation_update'),
    path('consultations/<int:pk>/supprimer/', crud_views.consultation_delete, name='consultation_delete'),
    path('factures/', invoices_list, name='factures'),
    path('facturation/', RedirectView.as_view(pattern_name='factures', permanent=False)),
    path('factures/ajouter/', crud_views.invoice_create, name='invoice_create'),
    path('factures/<int:pk>/modifier/', crud_views.invoice_update, name='invoice_update'),
    path('factures/<int:pk>/supprimer/', crud_views.invoice_delete, name='invoice_delete'),
    path('factures/<int:pk>/', payment_views.invoice_detail, name='facture_detail'),
    path('factures/<int:invoice_id>/payer/', payment_views.invoice_pay, name='invoice_pay'),
    path('factures/<int:invoice_id>/pdf/', invoice_pdf, name='invoice_pdf'),
    path('paiement/', payments_list, name='paiement'),
    path('paiements/', RedirectView.as_view(pattern_name='paiement', permanent=False)),
    path('services/', services_list, name='services'),
    path('services/ajouter/', crud_views.service_create, name='service_create'),
    path('services/<int:pk>/modifier/', crud_views.service_update, name='service_update'),
    path('services/<int:pk>/supprimer/', crud_views.service_delete, name='service_delete'),
    path('hospitalisation/', hospitalisation_list, name='hospitalisation'),
    path('laboratoire/', laboratoire_list, name='laboratoire'),
    path('laboratoire/<int:commande_id>/pdf/', labo_pdf, name='labo_pdf'),
    path('pharmacie/', pharmacie_list, name='pharmacie'),
    path('pharmacie/ajouter/', crud_views.medicament_create, name='medicament_create'),
    path('pharmacie/<int:pk>/modifier/', crud_views.medicament_update, name='medicament_update'),
    path('pharmacie/<int:pk>/supprimer/', crud_views.medicament_delete, name='medicament_delete'),
]
