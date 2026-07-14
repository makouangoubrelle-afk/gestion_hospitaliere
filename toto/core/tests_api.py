import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.mark.django_db
def test_sante_endpoint():
    client = Client()
    response = client.get('/api/v1/sante/')
    assert response.status_code == 200
    data = response.json()
    assert data['status'] in ('healthy', 'degraded')
    assert data['version'] == '1.0.0'


@pytest.mark.django_db
def test_jwt_login():
    User.objects.create_user(username='testuser', password='TestPass123!')
    client = Client()
    response = client.post(
        '/api/v1/auth/login',
        data='{"username":"testuser","password":"TestPass123!"}',
        content_type='application/json',
    )
    assert response.status_code == 200
    assert 'access' in response.json()


@pytest.mark.django_db
def test_lit_uniqueness_rule():
    from hospitalisation.models import Batiment, Chambre, Lit, ServiceHospitalier
    batiment = Batiment.objects.create(nom='Bloc A')
    service = ServiceHospitalier.objects.create(batiment=batiment, nom='Urgences', code='URG')
    chambre = Chambre.objects.create(service=service, numero='101')
    lit = Lit.objects.create(chambre=chambre, numero='1')
    assert lit.statut == 'disponible'
