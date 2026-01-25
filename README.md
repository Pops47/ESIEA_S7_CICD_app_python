# ESIEA_S7_CICD_app_python

Projet de pipeline CI/CD pour déployer une application Flask Python sur Kubernetes.

Le workflow GitHub Actions exécute des tests (linting, unitaires, intégration, performance), build et push l'image Docker vers GitHub Container Registry, convertit la configuration Docker Compose en manifests Kubernetes, génère les secrets depuis les secrets GitHub, et upload le package final sur un serveur FTP.

## Configuration

Avant d'utiliser le pipeline, configurez les secrets suivants dans les paramètres GitHub de votre repository :

- `FTP_HOST` : Adresse du serveur FTP
- `FTP_USER` : Utilisateur FTP
- `FTP_PASSWORD` : Mot de passe FTP
- `FTP_PATH` : Chemin du répertoire FTP de destination

- `APP_DB_PATH` (Facultatif) : Chemin de la base de données (par défaut sauvegarde locale sur /tmp/app.db)

Pour tester les manifests Kubernetes localement, vous pouvez utiliser minikube. Installation :

```bash
# macOS
brew install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Démarrer minikube
minikube start
```

## Utilisation

Le pipeline se déclenche automatiquement lors d'un push sur la branche `main`, ou manuellement via l'action `workflow_dispatch` dans l'onglet Actions de GitHub.

Une fois le workflow terminé, récupérez le fichier `PaulineSoubrieAppPython.zip` depuis le serveur FTP et décompressez-le. Les manifests Kubernetes sont prêts à être déployés :

```bash
kubectl apply -f PaulineSoubrieAppPython/
```

Puis pour visualiser l'API :

```bash
minikube service app --url
```

## Structure

Le projet contient :

- `app/` : Code source de l'application Flask (API REST)
- `docker-compose.yml` : Configuration du service avec 2 replicas
- `tests/` : Tests unitaires, d'intégration et de performance
- `.github/workflows/data-ci-cd.yml` : Pipeline CI/CD GitHub Actions
- Le workflow génère un dossier `PaulineSoubrieAppPython/` contenant tous les manifests Kubernetes (deployments, services, secrets, PVCs)
