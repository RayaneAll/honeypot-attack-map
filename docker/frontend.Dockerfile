# Dockerfile pour le frontend React + Vite + TailwindCSS
# Basé sur Node.js 18 pour la compatibilité

FROM node:18-alpine

# Métadonnées de l'image
LABEL maintainer="Honeypot Attack Map Team"
LABEL description="Frontend React pour la visualisation des attaques en temps réel"
LABEL version="1.0.0"

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apk add --no-cache \
    curl \
    git

# Copier le fichier package.json et package-lock.json d'abord pour optimiser le cache Docker
COPY frontend/package*.json ./

# Installer les dépendances npm
RUN npm ci --only=production --silent

# Copier le code source du frontend
COPY frontend/ .

# Créer un utilisateur non-root pour la sécurité
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 && \
    chown -R nextjs:nodejs /app

# Changer vers l'utilisateur non-root
USER nextjs

# Exposer le port 3000
EXPOSE 3000

# Variables d'environnement
ENV NODE_ENV=development
ENV VITE_API_URL=http://backend:8000
ENV VITE_WS_URL=ws://backend:8000
ENV VITE_APP_TITLE=Honeypot Attack Map
ENV VITE_APP_VERSION=1.0.0

# Health check pour vérifier que le frontend fonctionne
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:3000 || exit 1

# Commande par défaut pour lancer l'application en mode développement
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
