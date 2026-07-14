from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from ninja import Schema


class MessageSchema(Schema):
    detail: str


class TokenSchema(Schema):
    access: str
    refresh: str


class LoginSchema(Schema):
    username: str
    password: str


class UserOutSchema(Schema):
    id: int
    username: str
    role: str
    email: str = ''


class PatientInSchema(Schema):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    email: str
    phone: str
    address: str
    city: str
    postal_code: str
    country: str = 'Senegal'
    patient_id: str
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medical_history: Optional[str] = None


class PatientOutSchema(PatientInSchema):
    id: int
    status: str
    created_at: datetime


class MedecinOutSchema(Schema):
    id: int
    first_name: str
    last_name: str
    email: str
    specialty: str
    department: str
    status: str


class ConsultationInSchema(Schema):
    patient_id: int
    medecin_id: Optional[int] = None
    visit_type: str
    appointment_date: datetime
    chief_complaint: str
    diagnosis: Optional[str] = None
    cim10_code: Optional[str] = None
    treatment_plan: Optional[str] = None


class ConsultationOutSchema(ConsultationInSchema):
    id: int
    status: str


class HospitalisationInSchema(Schema):
    patient_id: int
    lit_id: int
    medecin_referent_id: int
    date_sortie_prevue: date
    motif: str


class HospitalisationOutSchema(HospitalisationInSchema):
    id: int
    statut: str
    date_entree: datetime


class CommandeLaboInSchema(Schema):
    patient_id: int
    medecin_prescripteur_id: int
    type_examen_id: int
    consultation_id: Optional[int] = None
    hospitalisation_id: Optional[int] = None
    numero_commande: str


class ResultatLaboInSchema(Schema):
    valeur: str
    unite: str = ''
    reference: str = ''


class PrescriptionInSchema(Schema):
    consultation_id: int
    medicament_id: int
    posologie: str
    duree_jours: int = 7
    quantite: int = 1


class RendezVousInSchema(Schema):
    patient_id: int
    medecin_id: int
    date_rdv: datetime
    motif: str = ''


class DashboardSchema(Schema):
    patients_actifs: int
    taux_occupation: float
    recettes_mois: Decimal
    examens_en_attente: int
    lits_disponibles: int
    lits_total: int
    consultations_du_jour: int


class SanteSchema(Schema):
    status: str
    version: str
    database: str
    timestamp: datetime
