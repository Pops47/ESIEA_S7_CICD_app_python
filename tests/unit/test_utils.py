"""Tests unitaires pour le module utils.py"""
import pytest
from app.utils import doThing, GLOBAL


class TestUtils:
    """Tests pour les fonctions utilitaires"""
    
    def setup_method(self):
        """Réinitialise l'état global avant chaque test"""
        GLOBAL["users"] = []
    
    def test_dothing_new_user(self):
        """Test doThing avec un nouvel utilisateur"""
        result = doThing("user1", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        
        assert result is True
        assert len(GLOBAL["users"]) == 1
        assert GLOBAL["users"][0]["name"] == "user1"
        assert GLOBAL["users"][0]["meta"] == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    def test_dothing_existing_user(self):
        """Test doThing avec un utilisateur existant (mise à jour)"""
        # Ajouter un utilisateur
        doThing("user1", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        
        # Mettre à jour avec de nouvelles valeurs
        result = doThing("user1", 10, 20, 30, 40, 50, 60, 70, 80, 90)
        
        assert result is True
        assert len(GLOBAL["users"]) == 1
        assert GLOBAL["users"][0]["name"] == "user1"
        assert GLOBAL["users"][0]["meta"] == [10, 20, 30, 40, 50, 60, 70, 80, 90]
    
    def test_dothing_multiple_users(self):
        """Test doThing avec plusieurs utilisateurs"""
        doThing("user1", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        doThing("user2", 10, 20, 30, 40, 50, 60, 70, 80, 90)
        
        assert len(GLOBAL["users"]) == 2
        assert GLOBAL["users"][0]["name"] == "user1"
        assert GLOBAL["users"][1]["name"] == "user2"
    
    def test_dothing_with_zero_values(self):
        """Test doThing avec des valeurs nulles"""
        result = doThing("user1", 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        assert result is True
        assert GLOBAL["users"][0]["meta"] == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    def test_dothing_with_negative_values(self):
        """Test doThing avec des valeurs négatives"""
        result = doThing("user1", -1, -2, -3, -4, -5, -6, -7, -8, -9)
        
        assert result is True
        assert GLOBAL["users"][0]["meta"] == [-1, -2, -3, -4, -5, -6, -7, -8, -9]
    
    def test_dothing_empty_name(self):
        """Test doThing avec un nom vide"""
        result = doThing("", 1, 2, 3, 4, 5, 6, 7, 8, 9)
        
        # La fonction devrait fonctionner même avec un nom vide
        assert result is True
        assert len(GLOBAL["users"]) == 1
