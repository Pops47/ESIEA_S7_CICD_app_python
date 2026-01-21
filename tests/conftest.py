"""Configuration globale pour pytest"""
import sys
import os

# Ajouter le répertoire racine au PYTHONPATH pour que les imports fonctionnent
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
