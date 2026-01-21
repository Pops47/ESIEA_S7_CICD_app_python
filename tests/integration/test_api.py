"""Tests d'intégration pour l'API Flask"""
import os
import tempfile
import pytest
from app.api import create_app
from app.db import init_db


@pytest.fixture
def app():
    """Fixture pour créer une application Flask de test"""
    # Créer une base de données temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    
    os.environ["APP_DB_PATH"] = db_path
    
    try:
        init_db()
        app = create_app()
        app.config['TESTING'] = True
        yield app
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
        if "APP_DB_PATH" in os.environ:
            del os.environ["APP_DB_PATH"]


@pytest.fixture
def client(app):
    """Fixture pour créer un client de test Flask"""
    return app.test_client()


class TestAPI:
    """Tests d'intégration pour l'API Flask"""
    
    def test_health_endpoint(self, client):
        """Test du endpoint /health"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
    
    def test_create_user(self, client):
        """Test de création d'un utilisateur"""
        response = client.post('/users', json={'name': 'Test User'})
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'id' in data
        assert isinstance(data['id'], int)
        assert data['id'] > 0
    
    def test_create_user_empty_name(self, client):
        """Test de création d'un utilisateur avec un nom vide"""
        response = client.post('/users', json={'name': ''})
        
        # Devrait retourner une erreur 500 car add_user lève une ValueError
        assert response.status_code == 500
    
    def test_create_user_no_json(self, client):
        """Test de création d'un utilisateur sans JSON"""
        response = client.post('/users')
        
        # Devrait quand même créer un utilisateur avec un nom vide
        # ce qui causera une erreur 500
        assert response.status_code == 500
    
    def test_get_user(self, client):
        """Test de récupération d'un utilisateur"""
        # Créer un utilisateur
        create_response = client.post('/users', json={'name': 'Test User'})
        user_id = create_response.get_json()['id']
        
        # Récupérer l'utilisateur
        response = client.get(f'/users/{user_id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == user_id
        assert data['name'] == 'Test User'
    
    def test_get_user_not_found(self, client):
        """Test de récupération d'un utilisateur inexistant"""
        response = client.get('/users/99999')
        
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'not found'
    
    def test_dothing_endpoint_success(self, client):
        """Test du endpoint /dothing avec des données valides"""
        payload = {
            'name': 'test_user',
            'meta': [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
        
        response = client.post('/dothing', json=payload)
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert data['result'] is True
    
    def test_dothing_endpoint_invalid_meta_length(self, client):
        """Test du endpoint /dothing avec une liste meta de mauvaise longueur"""
        payload = {
            'name': 'test_user',
            'meta': [1, 2, 3]  # Devrait être 9 valeurs
        }
        
        response = client.post('/dothing', json=payload)
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'meta must be a list of 9 values' in data['error']
    
    def test_dothing_endpoint_no_meta(self, client):
        """Test du endpoint /dothing sans meta"""
        payload = {
            'name': 'test_user'
        }
        
        response = client.post('/dothing', json=payload)
        
        assert response.status_code == 400
    
    def test_dothing_endpoint_meta_not_list(self, client):
        """Test du endpoint /dothing avec meta qui n'est pas une liste"""
        payload = {
            'name': 'test_user',
            'meta': 'not a list'
        }
        
        response = client.post('/dothing', json=payload)
        
        assert response.status_code == 400
    
    def test_dothing_endpoint_multiple_calls(self, client):
        """Test du endpoint /dothing avec plusieurs appels"""
        payload1 = {
            'name': 'test_user',
            'meta': [1, 2, 3, 4, 5, 6, 7, 8, 9]
        }
        
        payload2 = {
            'name': 'test_user',
            'meta': [10, 20, 30, 40, 50, 60, 70, 80, 90]
        }
        
        response1 = client.post('/dothing', json=payload1)
        assert response1.status_code == 200
        
        response2 = client.post('/dothing', json=payload2)
        assert response2.status_code == 200
    
    def test_full_user_workflow(self, client):
        """Test d'un workflow complet : création puis récupération"""
        # Créer un utilisateur
        create_response = client.post('/users', json={'name': 'Workflow User'})
        assert create_response.status_code == 201
        user_id = create_response.get_json()['id']
        
        # Récupérer l'utilisateur
        get_response = client.get(f'/users/{user_id}')
        assert get_response.status_code == 200
        assert get_response.get_json()['name'] == 'Workflow User'
        
        # Vérifier le health
        health_response = client.get('/health')
        assert health_response.status_code == 200
