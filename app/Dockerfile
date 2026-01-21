FROM python:3.11-slim

WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Créer le dossier app et copier les fichiers dedans pour préserver la structure des imports
RUN mkdir -p /app/app
COPY api.py db.py utils.py /app/app/

# Ajouter /app au PYTHONPATH pour que les imports fonctionnent
ENV PYTHONPATH=/app

# Exposer le port 8000
EXPOSE 8000

# Lancer l'application
CMD ["python", "app/api.py"]
