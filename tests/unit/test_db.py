"""Tests unitaires pour le module db.py"""
import os
import tempfile
import pytest
from app.db import init_db, add_user, get_user, get_db_path, User


class TestDB:
    """Tests pour les fonctions de base de données"""
    
    def test_get_db_path_default(self):
        """Test que le chemin par défaut est retourné si APP_DB_PATH n'est pas défini"""
        # Sauvegarder la valeur actuelle
        old_path = os.environ.get("APP_DB_PATH")
        if "APP_DB_PATH" in os.environ:
            del os.environ["APP_DB_PATH"]
        
        path = get_db_path()
        assert path == "/tmp/app.db"
        
        # Restaurer
        if old_path:
            os.environ["APP_DB_PATH"] = old_path
    
    def test_get_db_path_from_env(self):
        """Test que le chemin depuis l'environnement est utilisé"""
        test_path = "/tmp/test.db"
        os.environ["APP_DB_PATH"] = test_path
        
        path = get_db_path()
        assert path == test_path
        
        # Nettoyer
        del os.environ["APP_DB_PATH"]
    
    def test_init_db(self):
        """Test l'initialisation de la base de données"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name
        
        try:
            os.environ["APP_DB_PATH"] = db_path
            init_db()
            
            # Vérifier que le fichier existe
            assert os.path.exists(db_path)
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if "APP_DB_PATH" in os.environ:
                del os.environ["APP_DB_PATH"]
    
    def test_add_user(self):
        """Test l'ajout d'un utilisateur"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name
        
        try:
            os.environ["APP_DB_PATH"] = db_path
            init_db()
            
            user_id = add_user("Test User")
            assert isinstance(user_id, int)
            assert user_id > 0
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if "APP_DB_PATH" in os.environ:
                del os.environ["APP_DB_PATH"]
    
    def test_add_user_empty_name(self):
        """Test que l'ajout d'un nom vide lève une exception"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name
        
        try:
            os.environ["APP_DB_PATH"] = db_path
            init_db()
            
            with pytest.raises(ValueError, match="name must be non-empty"):
                add_user("")
            
            with pytest.raises(ValueError, match="name must be non-empty"):
                add_user("   ")
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if "APP_DB_PATH" in os.environ:
                del os.environ["APP_DB_PATH"]
    
    def test_get_user(self):
        """Test la récupération d'un utilisateur"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name
        
        try:
            os.environ["APP_DB_PATH"] = db_path
            init_db()
            
            user_id = add_user("Test User")
            user = get_user(user_id)
            
            assert user is not None
            assert isinstance(user, User)
            assert user.id == user_id
            assert user.name == "Test User"
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if "APP_DB_PATH" in os.environ:
                del os.environ["APP_DB_PATH"]
    
    def test_get_user_not_found(self):
        """Test la récupération d'un utilisateur inexistant"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name
        
        try:
            os.environ["APP_DB_PATH"] = db_path
            init_db()
            
            user = get_user(99999)
            assert user is None
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if "APP_DB_PATH" in os.environ:
                del os.environ["APP_DB_PATH"]
    
    def test_add_user_strips_whitespace(self):
        """Test que les espaces sont supprimés du nom"""
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp:
            db_path = tmp.name
        
        try:
            os.environ["APP_DB_PATH"] = db_path
            init_db()
            
            user_id = add_user("  Test User  ")
            user = get_user(user_id)
            
            assert user.name == "Test User"
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
            if "APP_DB_PATH" in os.environ:
                del os.environ["APP_DB_PATH"]
