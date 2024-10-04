# FastAPI Application

Ce projet est une API développée avec **FastAPI**. Cette application offre [brièvement décrire les fonctionnalités principales de l'application].

## Table des matières

1. [Prérequis](#prérequis)
2. [Installation](#installation)
3. [Variables d'environnement](#variables-denvironnement)
4. [Exécution du projet](#exécution-du-projet)
5. [Documentation API](#documentation-api)
6. [Déploiement](#déploiement)

---

## Prérequis

- **Python 3.8+** : Assurez-vous d'avoir Python 3.8 ou une version ultérieure installée sur votre machine.
- **Pip** : Un gestionnaire de paquets Python.
- **Virtualenv** (facultatif) : Pour isoler les dépendances dans un environnement virtuel.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/ton-utilisateur/ton-projet.git
cd ton-projet
```


### 2. Créer un environnement virtuel (optionnel mais recommandé)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Variables d'environnement

Créez un fichier .env à la racine du projet en suivant l'exemple ci-dessous et configurez les variables selon vos besoins :

```bash
# Exemple de configuration .env

APP_NAME="Name Application"
APP_DESCRIPTION="Description Application"
APP_VERSION="1.0.0"

# Cors polycies origin config
ALLOWED_ORIGINS=["http://localhost", "http://localhost:8000"]

# Environment
APP_ENV="developpement"

# Database Configuration
DATABASE_URL=mysql+mysqlconnector://username:password@host:3306/db_name

# SMTP CONNEXION
SMTP_SENDER_MAIL=""
SMTP_PASSWORD=""
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"

# Configuration authentication
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Exécution du projet

### Démarrer l'application en mode développement

Utilisez la commande suivante pour démarrer l'application en mode développement avec uvicorn :

```bash
uvicorn main:app --reload
```


## Documentation API

FastAPI génère automatiquement une documentation interactive via Swagger UI. Une fois l'application démarrée, accédez à la documentation via l'un des liens suivants :

- ***Swagger UI*** : http://127.0.0.1:8000/docs
- ***ReDoc*** : http://127.0.0.1:8000/redoc