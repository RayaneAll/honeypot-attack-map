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

2. **Lancer avec Docker Compose**
```bash
# Production
docker-compose up -d

# Développement
docker-compose -f docker-compose.dev.yml up -d
```

3. **Accéder à l'application**
- Frontend : http://localhost:3000
- Backend API : http://localhost:5000
- Health Check : http://localhost:5000/api/health

### Installation Locale

1. **Backend (Python)**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

pip install -r requirements.txt
python demo_data.py  # Générer des données de démo
python app.py
```

2. **Frontend (React)**
```bash
cd frontend
npm install
npm start
```

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

### Ports du Honeypot

Modifiez `HONEYPOT_PORTS` dans `backend/app.py` :
```python
HONEYPOT_PORTS = [22, 23, 80, 443, 3389, 5432, 3306]  # Ports à surveiller
```

### Géolocalisation

L'API utilise ip-api.com (gratuite, 1000 req/min). Pour changer :
```python
# Dans backend/geolocation.py
response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=5)
```

### Base de Données

- **Développement** : SQLite (par défaut)
- **Production** : PostgreSQL (voir docker-compose.yml)

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

#### Le honeypot ne détecte pas d'attaques
```bash
# Vérifier que les ports sont ouverts
netstat -tulpn | grep :22

# Tester la connexion
telnet localhost 22
```

#### Erreur de géolocalisation
```bash
# Vérifier la connectivité API
curl "http://ip-api.com/json/8.8.8.8"
```

#### Problème de WebSocket
```bash
# Vérifier les logs
docker-compose logs backend
```

### Logs
```bash
# Logs en temps réel
docker-compose logs -f

# Logs spécifiques
docker-compose logs backend
docker-compose logs frontend
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