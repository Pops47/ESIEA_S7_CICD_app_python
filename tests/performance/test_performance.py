"""Tests de performance pour l'application"""
import os
import tempfile
import pytest
from app.db import init_db, add_user, get_user
from app.utils import doThing, GLOBAL
from app.api import create_app


@pytest.fixture(autouse=True)
def reset_global():
    """Réinitialise l'état global avant chaque test"""
    GLOBAL["users"] = []
    yield
    GLOBAL["users"] = []


@pytest.fixture
def db_setup():
    """Fixture pour créer une base de données temporaire"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
        db_path = tmp.name
    
    os.environ["APP_DB_PATH"] = db_path
    
    try:
        init_db()
        yield db_path
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)
        if "APP_DB_PATH" in os.environ:
            del os.environ["APP_DB_PATH"]


class TestPerformance:
    """Tests de performance"""
    
    def test_add_user_performance(self, db_setup, benchmark):
        """Benchmark de l'ajout d'utilisateurs"""
        def add_test_user():
            add_user("Performance Test User")
        
        benchmark(add_test_user)
    
    def test_get_user_performance(self, db_setup, benchmark):
        """Benchmark de la récupération d'utilisateurs"""
        # Créer quelques utilisateurs d'abord
        user_ids = []
        for i in range(10):
            user_id = add_user(f"User {i}")
            user_ids.append(user_id)
        
        def get_test_user():
            get_user(user_ids[5])
        
        benchmark(get_test_user)
    
    def test_dothing_performance(self, benchmark):
        """Benchmark de la fonction doThing"""
        def do_test_thing():
            doThing("perf_user", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        
        benchmark(do_test_thing)
    
    def test_dothing_multiple_users_performance(self, benchmark):
        """Benchmark de doThing avec plusieurs utilisateurs"""
        # Préparer des utilisateurs
        for i in range(100):
            doThing(f"user_{i}", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        
        def do_test_thing_existing():
            doThing("user_50", 10, 20, 30, 40, 50, 60, 70, 80, 90)
        
        benchmark(do_test_thing_existing)
    
    def test_api_health_endpoint_performance(self, benchmark):
        """Benchmark du endpoint /health"""
        app = create_app()
        app.config['TESTING'] = True
        client = app.test_client()
        
        def get_health():
            client.get('/health')
        
        benchmark(get_health)
    
    def test_api_create_user_performance(self, db_setup, benchmark):
        """Benchmark du endpoint POST /users"""
        app = create_app()
        app.config['TESTING'] = True
        client = app.test_client()
        
        def create_user():
            client.post('/users', json={'name': 'Perf User'})
        
        benchmark(create_user)
    
    def test_api_get_user_performance(self, db_setup, benchmark):
        """Benchmark du endpoint GET /users/<id>"""
        app = create_app()
        app.config['TESTING'] = True
        client = app.test_client()
        
        # Créer un utilisateur
        response = client.post('/users', json={'name': 'Perf User'})
        user_id = response.get_json()['id']
        
        def get_user():
            client.get(f'/users/{user_id}')
        
        benchmark(get_user)
    
    def test_bulk_user_operations(self, db_setup):
        """Test de performance pour des opérations en masse"""
        import time
        
        # Test d'ajout en masse
        start = time.time()
        user_ids = []
        for i in range(100):
            user_id = add_user(f"Bulk User {i}")
            user_ids.append(user_id)
        add_time = time.time() - start
        
        # Test de récupération en masse
        start = time.time()
        for user_id in user_ids:
            get_user(user_id)
        get_time = time.time() - start
        
        # Les opérations ne devraient pas prendre trop de temps
        assert add_time < 1.0, f"L'ajout de 100 utilisateurs a pris {add_time}s (attendu < 1s)"
        assert get_time < 1.0, f"La récupération de 100 utilisateurs a pris {get_time}s (attendu < 1s)"
