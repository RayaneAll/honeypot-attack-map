# 🛡️ Honeypot Attack Map

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Un **Honeypot Visuel avec Attack Map en temps réel** pour visualiser les tentatives d'attaque en direct sur une carte interactive mondiale. Parfait pour les démonstrations de cybersécurité et les portfolios.

## 🎯 Fonctionnalités

- **🔥 Honeypot en temps réel** : Capture les tentatives de connexion sur plusieurs ports
- **🗺️ Carte interactive** : Visualisation des attaques sur une carte du monde avec Leaflet.js
- **📊 Dashboard temps réel** : Interface moderne avec WebSocket pour les mises à jour en direct
- **🌍 Géolocalisation IP** : Localisation automatique des adresses IP avec API gratuite
- **📈 Statistiques avancées** : Analyse des attaques par pays, protocole, et période
- **🔍 Filtrage intelligent** : Filtres par pays, protocole, et plage de temps
- **🐳 Docker Ready** : Déploiement facile avec Docker Compose
- **🧪 Tests inclus** : Suite de tests unitaires complète

## 🏗️ Architecture

```
honeypot-attack-map/
├── backend/                 # API Flask + Honeypot
│   ├── app.py              # Application principale
│   ├── models.py           # Modèles de base de données
│   ├── geolocation.py      # Service de géolocalisation
│   ├── demo_data.py        # Générateur de données de démo
│   └── requirements.txt    # Dépendances Python
├── frontend/               # Interface React
│   ├── src/
│   │   ├── components/     # Composants React
│   │   ├── App.js         # Application principale
│   │   └── index.js       # Point d'entrée
│   └── package.json       # Dépendances Node.js
├── tests/                  # Tests unitaires
├── docker-compose.yml     # Configuration Docker
└── README.md              # Documentation
```

## 🚀 Installation Rapide

### Prérequis
- Docker et Docker Compose
- Python 3.11+ (pour développement local)
- Node.js 18+ (pour développement local)

### Déploiement avec Docker (Recommandé)

1. **Cloner le projet**
```bash
git clone https://github.com/votre-username/honeypot-attack-map.git
cd honeypot-attack-map
```

2. **Construire et lancer les conteneurs**
```bash
# Méthode recommandée avec scripts
./scripts/docker-start.sh dev    # Mode développement
./scripts/docker-start.sh prod   # Mode production
./scripts/docker-start.sh demo   # Mode démonstration

# Ou méthode manuelle
docker-compose build
docker-compose up -d
```

3. **Accéder à l'application**
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **API Documentation** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/health

4. **Vérifier le statut des services**
```bash
# Avec scripts (recommandé)
./scripts/docker-logs.sh          # Voir tous les logs
./scripts/docker-logs.sh backend  # Logs du backend uniquement
./scripts/docker-stop.sh --status # Statut des services

# Ou méthode manuelle
docker-compose logs -f
docker-compose ps
docker-compose down
```

### Installation Locale

1. **Backend (Python)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

pip install -r requirements.txt
python init_db.py  # Initialiser la base de données
python populate_fake_attacks.py  # Générer des données de démo
python main.py
```

2. **Frontend (React)**
```bash
cd frontend
npm install
npm run dev
```

## 🐳 Configuration Docker

### Fichiers Docker

Le projet utilise une architecture Docker modulaire :

```
docker/
├── backend.Dockerfile      # Image FastAPI + SQLite
├── frontend.Dockerfile     # Image React + Vite
├── docker-compose.yml      # Configuration production
├── docker-compose.dev.yml  # Configuration développement
└── docker-compose.prod.yml # Configuration production avancée
```

### Services Docker

#### Backend Service
- **Image** : Python 3.10-slim
- **Port** : 8000
- **Base de données** : SQLite (persistante)
- **Health check** : `/health` endpoint
- **Volumes** : Données persistantes

#### Frontend Service
- **Image** : Node.js 18-alpine
- **Port** : 3000
- **Build** : Vite + TailwindCSS
- **Communication** : WebSocket vers backend
- **Volumes** : Code source (mode dev)

### Commandes Docker Utiles

#### Scripts Automatisés (Recommandé)
```bash
# Démarrer le projet
./scripts/docker-start.sh [dev|prod|demo]

# Arrêter le projet
./scripts/docker-stop.sh [--clean|--images|--full]

# Voir les logs
./scripts/docker-logs.sh [service] [options]
```

#### Commandes Docker Compose
```bash
# Construire les images
docker-compose build

# Lancer en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Redémarrer un service
docker-compose restart backend

# Arrêter tous les services
docker-compose down

# Supprimer les volumes (ATTENTION: supprime les données)
docker-compose down -v

# Nettoyer les images
docker-compose down --rmi all
```

### Modes de Déploiement

#### Mode Production
```bash
docker-compose up -d
```
- Services optimisés
- Logs réduits
- Restart automatique
- Volumes persistants

#### Mode Développement
```bash
docker-compose -f docker/docker-compose.dev.yml up -d
```
- Code source monté
- Hot reload activé
- Logs détaillés
- Debug facilité

#### Mode Démonstration
```bash
docker-compose --profile demo up -d
```
- Données de test générées
- Interface pré-remplie
- Parfait pour les démos

## 📖 Guide d'Utilisation

### 1. Génération de Données de Démonstration

Pour tester l'application sans vraies attaques :

```bash
cd backend
python demo_data.py
```

Ce script génère :
- 200 attaques historiques sur 7 jours
- 15 attaques récentes pour le temps réel
- Données géolocalisées réalistes

### 2. Interface Utilisateur

#### Carte Interactive
- **Points rouges** : Attaques détectées en temps réel
- **Clic sur un point** : Détails de l'attaque (IP, port, localisation)
- **Zoom/Pan** : Navigation libre sur la carte

#### Panneau de Contrôle
- **Statistiques** : Nombre total d'attaques, attaques 24h
- **Top Pays** : Classement des pays par nombre d'attaques
- **Filtres** : Par pays, protocole, période
- **Liste des Attaques** : Historique en temps réel

### 3. API Endpoints

#### GET /api/attacks
Récupère les attaques récentes
```bash
curl "http://localhost:5000/api/attacks?limit=50&country=USA&protocol=SSH"
```

#### GET /api/stats
Statistiques des attaques
```bash
curl "http://localhost:5000/api/stats"
```

#### GET /api/health
État de santé du système
```bash
curl "http://localhost:5000/api/health"
```

### 4. WebSocket (Temps Réel)

Connexion WebSocket pour les mises à jour en direct :
```javascript
const socket = io('http://localhost:5000');
socket.on('new_attack', (attack) => {
    console.log('Nouvelle attaque:', attack);
});
```

## 🔧 Configuration

### Variables d'Environnement Docker

#### Backend
```env
PYTHONPATH=/app
PYTHONUNBUFFERED=1
DATABASE_URL=sqlite:///./data/honeypot_attacks.db
HONEYPOT_PORT=2222
GEOIP_API_URL=http://ip-api.com/json
LOG_LEVEL=INFO
```

#### Frontend
```env
NODE_ENV=development
VITE_API_URL=http://backend:8000
VITE_WS_URL=ws://backend:8000
VITE_APP_TITLE=Honeypot Attack Map
VITE_APP_VERSION=1.0.0
```

### Ports du Honeypot

Modifiez `HONEYPOT_PORTS` dans `backend/main.py` :
```python
HONEYPOT_PORTS = [22, 23, 80, 443, 3389, 5432, 3306]  # Ports à surveiller
```

### Géolocalisation

L'API utilise ip-api.com (gratuite, 1000 req/min). Pour changer :
```python
# Dans backend/services/geoip.py
response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
```

### Base de Données

- **Développement** : SQLite (par défaut)
- **Production** : SQLite persistante dans Docker
- **Volume** : `honeypot_backend_data`

### Communication Inter-Conteneurs

Les services communiquent via le réseau Docker interne :
- **Backend** : `http://backend:8000`
- **Frontend** : `http://frontend:3000`
- **WebSocket** : `ws://backend:8000`

## 🧪 Tests

Lancer tous les tests :
```bash
cd tests
python run_tests.py
```

Tests individuels :
```bash
python -m unittest test_models.py
python -m unittest test_api.py
python -m unittest test_geolocation.py
```

## 📊 Captures d'Écran

### Dashboard Principal
![Dashboard](screenshots/dashboard.png)
*Interface principale avec carte interactive et statistiques*

### Détails d'Attaque
![Attack Details](screenshots/attack-details.png)
*Popup détaillant une attaque spécifique*

### Filtres et Statistiques
![Filters](screenshots/filters.png)
*Panneau de filtrage et statistiques avancées*

## 🔒 Sécurité

⚠️ **Important** : Ce projet est destiné à des fins éducatives et de démonstration.

- Ne déployez pas sur des serveurs de production
- Utilisez uniquement dans des environnements isolés
- Les données d'attaque sont stockées localement
- Aucune donnée sensible n'est collectée

## 🛠️ Développement

### Structure du Code

#### Backend (Flask)
- `app.py` : Application principale avec routes API et WebSocket
- `models.py` : Modèles de base de données SQLite
- `geolocation.py` : Service de géolocalisation IP
- `demo_data.py` : Générateur de données de test

#### Frontend (React)
- `App.js` : Composant principal avec gestion d'état
- `AttackMap.js` : Carte Leaflet avec marqueurs d'attaques
- `AttackList.js` : Liste des attaques récentes
- `StatsPanel.js` : Panneau de statistiques
- `FilterPanel.js` : Interface de filtrage

### Ajout de Nouveaux Ports

1. Modifier `HONEYPOT_PORTS` dans `backend/app.py`
2. Redémarrer le backend
3. Les nouveaux ports seront automatiquement surveillés

### Personnalisation de l'Interface

Modifiez les composants React dans `frontend/src/components/` :
- Couleurs : `tailwind.config.js`
- Styles : `frontend/src/index.css`
- Composants : `frontend/src/components/`

## 📈 Performance

### Optimisations Incluses
- **Cache de géolocalisation** : Évite les appels API répétés
- **Index de base de données** : Requêtes optimisées
- **Pagination** : Limite des résultats (100 par défaut)
- **Compression Gzip** : Réduction de la bande passante
- **WebSocket** : Mises à jour en temps réel efficaces

### Monitoring
- Health checks Docker
- Logs structurés
- Métriques de performance

## 🐛 Dépannage

### Problèmes Courants

#### Les conteneurs ne démarrent pas
```bash
# Vérifier les logs de build
docker-compose build --no-cache

# Vérifier les logs de démarrage
docker-compose logs

# Redémarrer les services
docker-compose restart
```

#### Le honeypot ne détecte pas d'attaques
```bash
# Vérifier que le backend est en cours d'exécution
docker-compose ps backend

# Tester la connexion au honeypot
telnet localhost 2222

# Vérifier les logs du backend
docker-compose logs backend
```

#### Erreur de géolocalisation
```bash
# Vérifier la connectivité API depuis le conteneur
docker-compose exec backend curl "http://ip-api.com/json/8.8.8.8"

# Vérifier les logs
docker-compose logs backend | grep geoip
```

#### Problème de WebSocket
```bash
# Vérifier la connexion WebSocket
docker-compose exec frontend curl -I http://backend:8000/ws

# Vérifier les logs
docker-compose logs frontend | grep websocket
```

#### Frontend ne se connecte pas au backend
```bash
# Vérifier la connectivité réseau
docker-compose exec frontend ping backend

# Vérifier les variables d'environnement
docker-compose exec frontend env | grep VITE_API_URL

# Tester l'API depuis le frontend
docker-compose exec frontend curl http://backend:8000/health
```

### Logs et Debugging

```bash
# Logs en temps réel
docker-compose logs -f

# Logs spécifiques
docker-compose logs backend
docker-compose logs frontend

# Logs avec timestamps
docker-compose logs -f -t

# Logs des 100 dernières lignes
docker-compose logs --tail=100 backend
```

### Commandes de Maintenance

```bash
# Nettoyer les conteneurs arrêtés
docker-compose down

# Supprimer les volumes (ATTENTION: supprime les données)
docker-compose down -v

# Nettoyer les images inutilisées
docker system prune -a

# Reconstruire sans cache
docker-compose build --no-cache

# Vérifier l'utilisation des ressources
docker stats
```

### Problèmes de Performance

```bash
# Vérifier l'utilisation des ressources
docker stats

# Vérifier l'espace disque
docker system df

# Nettoyer l'espace disque
docker system prune -a --volumes
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- [Leaflet.js](https://leafletjs.com/) pour la carte interactive
- [ip-api.com](http://ip-api.com/) pour la géolocalisation gratuite
- [React](https://reactjs.org/) pour l'interface utilisateur
- [Flask](https://flask.palletsprojects.com/) pour l'API backend
- [Tailwind CSS](https://tailwindcss.com/) pour le styling

## 📞 Support

Pour toute question ou problème :
- Ouvrir une [issue](https://github.com/votre-username/honeypot-attack-map/issues)
- Email : votre-email@example.com

---

**⚡ Développé avec passion pour la cybersécurité et la visualisation de données**