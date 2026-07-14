from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import Role, UserProfile
from consultations.models import Consultation
from core.models import PlanningGarde, RendezVous
from factures.models import Invoice, InvoiceItem
from hospitalisation.models import Batiment, Chambre, Hospitalisation, Lit, ServiceHospitalier
from laboratoire.models import CommandeLabo, Prelevement, ResultatLabo, TypeExamen
from geolocalisation.models import SiteLocalise
from infirmiers.models import Infirmier
from medecins.models import Medecin
from organisation.models import FileAttente, SalleAttente, SalleUrgence
from paiement.models import Payment, PaymentMethod
from patients.models import Patient
from pharmacie.models import Medicament, Prescription
from secretaires.models import Secretaire
from services.models import Service, ServicePrice


class Command(BaseCommand):
    help = 'Charge des données de démonstration pour la soutenance SGHL'

    def handle(self, *args, **options):
        self.stdout.write('Chargement des données de démo SGHL...')

        users = self._create_users()
        patients = self._create_patients()
        medecins = self._create_medecins()
        self._create_infirmiers()
        self._create_secretaires()
        self._create_geolocalisation()
        self._link_user_profiles(users, patients, medecins)
        lits = self._create_hospital_structure()
        consultations = self._create_consultations(patients, medecins)
        self._create_hospitalisation(patients[2], medecins[0], lits[0])
        self._create_laboratoire(patients, medecins, consultations)
        self._create_pharmacie(consultations)
        self._create_facturation(patients, consultations)
        self._create_payment_gateways()
        self._create_services()
        self._create_planning(medecins, lits)
        self._create_rendez_vous(patients, medecins)
        self._create_salles(patients, medecins)

        self.stdout.write(self.style.SUCCESS('Données de démo chargées avec succès !'))
        self.stdout.write('')
        self.stdout.write('Comptes de test :')
        for role, password in [
            ('admin', 'Admin123!'),
            ('medecin', 'Medecin123!'),
            ('biologiste', 'Bio123!'),
            ('secretaire', 'Secretaire123!'),
            ('patient', 'Patient123!'),
        ]:
            self.stdout.write(f'  - {role} / {password}')

    def _create_users(self):
        users = {}
        for username, role, email in [
            ('admin', Role.ADMIN, 'admin@sghl.sn'),
            ('medecin', Role.MEDECIN, 'medecin@sghl.sn'),
            ('biologiste', Role.BIOLOGISTE, 'bio@sghl.sn'),
            ('infirmier', Role.INFIRMIER, 'infirmier@sghl.sn'),
            ('pharmacien', Role.PHARMACIEN, 'pharma@sghl.sn'),
            ('comptable', Role.COMPTABLE, 'compta@sghl.sn'),
            ('secretaire', Role.SECRETAIRE, 'secretaire@sghl.sn'),
            ('patient', Role.PATIENT, 'patient@sghl.sn'),
        ]:
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password(f'{username.capitalize()}123!' if username != 'admin' else 'Admin123!')
                if username == 'biologiste':
                    user.set_password('Bio123!')
                if username == 'patient':
                    user.set_password('Patient123!')
                user.save()
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
            users[username] = user
        return users

    def _create_patients(self):
        data = [
            ('PAT-001', 'Amadou', 'Diallo', 'M', 'amadou.diallo@email.sn'),
            ('PAT-002', 'Fatou', 'Sow', 'F', 'fatou.sow@email.sn'),
            ('PAT-003', 'Moussa', 'Ndiaye', 'M', 'moussa.ndiaye@email.sn'),
        ]
        patients = []
        for pid, first, last, gender, email in data:
            patient, _ = Patient.objects.get_or_create(
                patient_id=pid,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'date_of_birth': timezone.now().date().replace(year=1985),
                    'gender': gender,
                    'email': email,
                    'phone': '+221771234567',
                    'address': '12 Avenue Léopold Sédar Senghor',
                    'city': 'Dakar',
                    'postal_code': '10000',
                    'blood_type': 'O+',
                    'allergies': 'Pénicilline' if pid == 'PAT-001' else '',
                    'medical_history': 'Hypertension légère' if pid == 'PAT-002' else '',
                },
            )
            patients.append(patient)
        return patients

    def _create_medecins(self):
        data = [
            ('LIC-001', 'Cheikh', 'Mbaye', 'cardiology', 'Cardiologie'),
            ('LIC-002', 'Aissatou', 'Fall', 'pediatrics', 'Pédiatrie'),
        ]
        medecins = []
        for lic, first, last, specialty, dept in data:
            medecin, _ = Medecin.objects.get_or_create(
                license_number=lic,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{first.lower()}.{last.lower()}@sghl.sn',
                    'phone': '+221779876543',
                    'specialty': specialty,
                    'department': dept,
                    'years_experience': 12,
                },
            )
            medecins.append(medecin)
        return medecins

    def _create_infirmiers(self):
        data = [
            ('INF-001', 'Awa', 'Diop', 'urgences', 'ide', 'Urgences adultes', 'Jour 7h-19h'),
            ('INF-002', 'Mamadou', 'Ba', 'reanimation', 'ide', 'Réanimation', 'Nuit 19h-7h'),
            ('INF-003', 'Coumba', 'Gueye', 'pediatrie', 'cadre', 'Pédiatrie', 'Jour 7h-15h'),
        ]
        for matricule, first, last, service, grade, unite, shift in data:
            Infirmier.objects.get_or_create(
                matricule=matricule,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{first.lower()}.{last.lower()}@sghl.sn',
                    'phone': '+221771112233',
                    'service': service,
                    'grade': grade,
                    'unite': unite,
                    'shift': shift,
                    'years_experience': 8,
                    'status': 'active',
                },
            )

    def _create_secretaires(self):
        data = [
            ('SEC-001', 'Fatou', 'Ndiaye', 'Guichet 1', 'Accueil général', 'Lun–Ven 8h–17h'),
            ('SEC-002', 'Ibrahima', 'Sow', 'Guichet 2', 'Urgences', '24h/24'),
            ('SEC-003', 'Aminata', 'Fall', 'Guichet 3', 'Consultations', 'Lun–Sam 7h–19h'),
        ]
        for matricule, first, last, bureau, service, horaires in data:
            Secretaire.objects.get_or_create(
                matricule=matricule,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{first.lower()}.{last.lower()}@sghl.sn',
                    'phone': '+221771234567',
                    'bureau': bureau,
                    'service_accueil': service,
                    'horaires': horaires,
                    'status': 'active',
                },
            )

    def _create_geolocalisation(self):
        sites = [
            (
                'SGHL — Hôpital principal',
                'hopital',
                '12 Avenue Léopold Sédar Senghor, Plateau',
                'Dakar',
                '14.670000',
                '-17.438000',
                '+221338211111',
            ),
            (
                'SGHL — Laboratoire central',
                'laboratoire',
                '45 Rue de la République',
                'Dakar',
                '14.693700',
                '-17.444100',
                '+221338222222',
            ),
            (
                'SGHL — Pharmacie hospitalière',
                'pharmacie',
                'Avenue Cheikh Anta Diop',
                'Dakar',
                '14.716700',
                '-17.467700',
                '+221338233333',
            ),
            (
                'Unité mobile urgences',
                'ambulance',
                'Déploiement zone Pikine',
                'Pikine',
                '14.754900',
                '-17.390600',
                '+221338244444',
            ),
        ]
        for nom, type_lieu, adresse, ville, lat, lng, tel in sites:
            SiteLocalise.objects.get_or_create(
                nom=nom,
                defaults={
                    'type_lieu': type_lieu,
                    'adresse': adresse,
                    'ville': ville,
                    'latitude': Decimal(lat),
                    'longitude': Decimal(lng),
                    'telephone': tel,
                    'description': f'Site SGHL — {ville}',
                    'is_active': True,
                },
            )

    def _link_user_profiles(self, users, patients, medecins):
        users['medecin'].profile.medecin = medecins[0]
        users['medecin'].profile.save()
        users['patient'].profile.patient = patients[0]
        users['patient'].profile.save()

    def _create_hospital_structure(self):
        batiment, _ = Batiment.objects.get_or_create(nom='Bloc Principal', defaults={'adresse': 'Hôpital SGHL, Dakar'})
        service, _ = ServiceHospitalier.objects.get_or_create(
            batiment=batiment, code='CARD',
            defaults={'nom': 'Cardiologie', 'description': 'Service de cardiologie'},
        )
        ServiceHospitalier.objects.get_or_create(
            batiment=batiment, code='URG',
            defaults={'nom': 'Urgences', 'description': 'Service des urgences'},
        )
        chambre, _ = Chambre.objects.get_or_create(service=service, numero='201', defaults={'etage': 2, 'capacite': 2})
        chambre2, _ = Chambre.objects.get_or_create(service=service, numero='202', defaults={'etage': 2, 'capacite': 2})
        lit1, _ = Lit.objects.get_or_create(chambre=chambre, numero='A', defaults={'statut': Lit.Statut.DISPONIBLE})
        Lit.objects.get_or_create(chambre=chambre, numero='B', defaults={'statut': Lit.Statut.DISPONIBLE})
        Lit.objects.get_or_create(chambre=chambre2, numero='A', defaults={'statut': Lit.Statut.DISPONIBLE})
        return [lit1]

    def _create_consultations(self, patients, medecins):
        now = timezone.now()
        consultations = []
        specs = [
            (patients[0], medecins[0], 'Douleurs thoraciques', 'I10', 'Hypertension essentielle', 'completed'),
            (patients[1], medecins[1], 'Fièvre et toux', 'J06.9', 'Infection respiratoire', 'completed'),
            (patients[0], medecins[0], 'Contrôle post-traitement', 'I10', 'Suivi hypertension', 'scheduled'),
        ]
        for i, (patient, medecin, complaint, cim10, diagnosis, status) in enumerate(specs):
            consultation, _ = Consultation.objects.get_or_create(
                patient=patient,
                medecin=medecin,
                appointment_date=now - timedelta(days=5 - i),
                defaults={
                    'visit_type': 'outpatient',
                    'chief_complaint': complaint,
                    'cim10_code': cim10,
                    'diagnosis': diagnosis,
                    'treatment_plan': 'Traitement adapté et suivi régulier',
                    'status': status,
                },
            )
            consultations.append(consultation)
        return consultations

    def _create_hospitalisation(self, patient, medecin, lit):
        if Hospitalisation.objects.filter(patient=patient, statut=Hospitalisation.Statut.ACTIVE).exists():
            return
        Hospitalisation.objects.create(
            patient=patient,
            lit=lit,
            medecin_referent=medecin,
            date_sortie_prevue=(timezone.now() + timedelta(days=5)).date(),
            motif='Surveillance post-infarctus',
        )

    def _create_laboratoire(self, patients, medecins, consultations):
        types = [
            ('NFS', 'Numération formule sanguine', 15000),
            ('GLY', 'Glycémie à jeun', 8000),
            ('CRP', 'Protéine C-réactive', 12000),
        ]
        examens = []
        for code, nom, prix in types:
            examen, _ = TypeExamen.objects.get_or_create(
                code=code, defaults={'nom': nom, 'prix': Decimal(str(prix))},
            )
            examens.append(examen)

        commande, _ = CommandeLabo.objects.get_or_create(
            numero_commande='LAB-2026-001',
            defaults={
                'patient': patients[0],
                'consultation': consultations[0],
                'medecin_prescripteur': medecins[0],
                'type_examen': examens[0],
                'statut': CommandeLabo.Statut.SAISIE,
            },
        )
        Prelevement.objects.get_or_create(
            commande=commande,
            defaults={'echantillon_id': 'ECH-001', 'notes': 'Prélèvement veineux'},
        )
        ResultatLabo.objects.get_or_create(
            commande=commande,
            defaults={
                'valeur': '14.2',
                'unite': 'g/dL',
                'reference': '12.0 - 16.0',
            },
        )

        CommandeLabo.objects.get_or_create(
            numero_commande='LAB-2026-002',
            defaults={
                'patient': patients[1],
                'consultation': consultations[1],
                'medecin_prescripteur': medecins[1],
                'type_examen': examens[1],
                'statut': CommandeLabo.Statut.COMMANDEE,
            },
        )

    def _create_pharmacie(self, consultations):
        from pharmacie.seed_utils import seed_medicament_catalog

        seed_medicament_catalog()

        Prescription.objects.get_or_create(
            consultation=consultations[0],
            medicament=Medicament.objects.get(code='AMLO5'),
            defaults={'posologie': '1 cp/jour le matin', 'quantite': 30, 'statut': 'validee'},
        )

    def _create_facturation(self, patients, consultations):
        invoice, created = Invoice.objects.get_or_create(
            invoice_number='FAC-2026-001',
            defaults={
                'patient': patients[0],
                'consultation': consultations[0],
                'due_date': (timezone.now() + timedelta(days=30)).date(),
                'subtotal': Decimal('45000'),
                'tax': Decimal('0'),
                'total_amount': Decimal('45000'),
                'paid_amount': Decimal('20000'),
                'status': 'partial',
                'assurance_nom': 'CNAM Senegal',
                'assurance_numero': 'CNAM-789456',
                'montant_assurance': Decimal('30000'),
                'montant_patient': Decimal('15000'),
                'description': 'Consultation cardiologie + examens',
            },
        )
        if created:
            InvoiceItem.objects.create(
                invoice=invoice,
                description='Consultation cardiologie',
                quantity=1,
                unit_price=Decimal('25000'),
                subtotal=Decimal('25000'),
            )
            InvoiceItem.objects.create(
                invoice=invoice,
                description='NFS laboratoire',
                quantity=1,
                unit_price=Decimal('15000'),
                subtotal=Decimal('15000'),
            )
            Payment.objects.get_or_create(
                transaction_id='PAY-001',
                defaults={
                    'invoice': invoice,
                    'payment_method': 'mtn_momo',
                    'amount': Decimal('20000'),
                    'status': 'completed',
                    'payment_date': timezone.now(),
                    'phone_number': '+221771234567',
                },
            )

        Invoice.objects.get_or_create(
            invoice_number='FAC-2026-002',
            defaults={
                'patient': patients[1],
                'consultation': consultations[1],
                'due_date': (timezone.now() + timedelta(days=15)).date(),
                'subtotal': Decimal('18000'),
                'tax': Decimal('0'),
                'total_amount': Decimal('18000'),
                'status': 'sent',
                'description': 'Consultation pédiatrie',
            },
        )

    def _create_payment_gateways(self):
        for gateway in ('mtn_momo', 'airtel_money', 'stripe'):
            PaymentMethod.objects.get_or_create(gateway=gateway, defaults={'is_active': True})

    def _create_services(self):
        service, _ = Service.objects.get_or_create(
            code='CONS-GEN',
            defaults={'name': 'Consultation générale', 'description': 'Consultation médicale standard'},
        )
        ServicePrice.objects.get_or_create(
            service=service,
            name='Consultation standard',
            defaults={'price': Decimal('15000'), 'description': 'Tarif standard'},
        )

    def _create_planning(self, medecins, lits):
        service = ServiceHospitalier.objects.first()
        if service and not PlanningGarde.objects.exists():
            now = timezone.now()
            PlanningGarde.objects.create(
                medecin=medecins[0],
                service=service,
                date_debut=now.replace(hour=8, minute=0),
                date_fin=now.replace(hour=20, minute=0),
                notes='Garde cardiologie',
            )

    def _create_rendez_vous(self, patients, medecins):
        RendezVous.objects.get_or_create(
            patient=patients[0],
            medecin=medecins[0],
            date_rdv=timezone.now() + timedelta(days=7),
            defaults={'motif': 'Contrôle tension artérielle', 'statut': 'confirme'},
        )

    def _create_salles(self, patients, medecins):
        urgences = [
            ('URG-01', 'Box traumatologie', 4, SalleUrgence.Statut.OCCUPEE, patients[0], medecins[0]),
            ('URG-02', 'Box réanimation', 2, SalleUrgence.Statut.LIBRE, None, None),
            ('URG-03', 'Box pédiatrie', 3, SalleUrgence.Statut.MAINTENANCE, None, None),
        ]
        for code, nom, capacite, statut, patient, medecin in urgences:
            SalleUrgence.objects.get_or_create(
                code=code,
                defaults={
                    'nom': nom,
                    'capacite': capacite,
                    'statut': statut,
                    'patient': patient,
                    'medecin': medecin,
                },
            )

        attentes = [
            ('ATT-01', 'Salle accueil principal', 40, 'Hall A'),
            ('ATT-02', 'Salle urgences', 25, 'Urgences'),
            ('ATT-03', 'Salle consultations', 30, 'Consultations'),
        ]
        salles = {}
        for code, nom, capacite, zone in attentes:
            salle, _ = SalleAttente.objects.get_or_create(
                code=code,
                defaults={'nom': nom, 'capacite': capacite, 'zone': zone},
            )
            salles[code] = salle

        files = [
            (salles['ATT-01'], patients[1], 'Consultation générale', FileAttente.Priorite.NORMALE),
            (salles['ATT-02'], patients[2], 'Douleur thoracique', FileAttente.Priorite.URGENTE),
        ]
        for salle, patient, motif, priorite in files:
            FileAttente.objects.get_or_create(
                salle_attente=salle,
                patient=patient,
                statut=FileAttente.Statut.EN_ATTENTE,
                defaults={'motif': motif, 'priorite': priorite},
            )
