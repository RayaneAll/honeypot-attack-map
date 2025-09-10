# Dockerfile pour le backend FastAPI + SQLite
# Basé sur Python 3.10 slim pour une image légère

FROM python:3.10-slim

# Métadonnées de l'image
LABEL maintainer="Honeypot Attack Map Team"
LABEL description="Backend FastAPI pour le système de visualisation d'attaques"
LABEL version="1.0.0"

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copier le fichier requirements.txt d'abord pour optimiser le cache Docker
COPY backend/requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source du backend
COPY backend/ .

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app

# Créer le répertoire pour la base de données
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port 8000
EXPOSE 8000

# Variables d'environnement
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./data/honeypot_attacks.db

# Health check pour vérifier que l'API fonctionne
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Commande par défaut pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
