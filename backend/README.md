# 🛡️ Honeypot Attack Map - Backend

Backend FastAPI pour le système de visualisation d'attaques en temps réel avec honeypot TCP.

## 🎯 Vue d'ensemble

Ce backend fournit :
- **Honeypot TCP** qui écoute sur un port et capture les tentatives de connexion
- **API REST** pour accéder aux données d'attaques
- **WebSocket** pour les mises à jour en temps réel
- **Géolocalisation IP** automatique via API gratuite
- **Base de données SQLite** avec SQLAlchemy ORM

## 🏗️ Architecture

```
backend/
├── main.py                 # Application FastAPI principale
├── honeypot.py            # Serveur honeypot TCP
├── models.py              # Modèles SQLAlchemy
├── database.py            # Configuration base de données
├── routes/
│   └── attacks.py         # Endpoints REST API
├── services/
│   └── geoip.py           # Service de géolocalisation
├── tests/
│   └── test_api.py        # Tests unitaires
├── init_db.py             # Script d'initialisation
├── populate_fake_attacks.py # Générateur de données de test
└── requirements.txt       # Dépendances Python
```

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.11+
- pip

### Installation

1. **Cloner le projet**
```bash
git clone <repository-url>
cd honeypot-attack-map/backend
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Initialiser la base de données**
```bash
python init_db.py
```

5. **Générer des données de test (optionnel)**
```bash
python populate_fake_attacks.py
```

6. **Lancer le serveur**
```bash
python main.py
```

### Accès à l'API

- **API Documentation** : http://localhost:8000/docs
- **API Alternative** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health
- **WebSocket** : ws://localhost:8000/ws

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` :
```env
DATABASE_URL=sqlite:///./honeypot_attacks.db
HONEYPOT_PORT=2222
GEOIP_API_URL=http://ip-api.com/json
LOG_LEVEL=INFO
```

### Ports du Honeypot

Modifier dans `main.py` :
```python
honeypot_server = HoneypotServer(
    port=2222,  # Changer le port ici
    on_attack_callback=handle_new_attack
)
```

## 📡 API Endpoints

### Endpoints Principaux

#### `GET /`
Informations générales sur l'API

#### `GET /health`
Vérification de l'état de santé

#### `GET /stats`
Statistiques générales des attaques

### Endpoints des Attaques

#### `GET /api/attacks/`
Récupère la liste des attaques

**Paramètres de requête :**
- `limit` (int, optionnel) : Nombre maximum d'attaques (défaut: 100)
- `offset` (int, optionnel) : Décalage pour pagination (défaut: 0)
- `country` (str, optionnel) : Filtrer par pays
- `protocol` (str, optionnel) : Filtrer par protocole
- `port` (int, optionnel) : Filtrer par port
- `hours` (int, optionnel) : Filtrer les attaques des dernières X heures

**Exemple :**
```bash
curl "http://localhost:8000/api/attacks/?limit=50&country=United States&protocol=SSH"
```

#### `GET /api/attacks/{attack_id}`
Récupère une attaque spécifique par ID

#### `GET /api/attacks/stats/summary`
Résumé des statistiques d'attaques

#### `GET /api/attacks/stats/by-country`
Statistiques par pays

#### `GET /api/attacks/stats/by-port`
Statistiques par port

#### `GET /api/attacks/recent/live`
Attaques très récentes (pour temps réel)

#### `DELETE /api/attacks/{attack_id}`
Supprime une attaque spécifique

#### `DELETE /api/attacks/cleanup/old`
Nettoie les anciennes attaques

## 🔌 WebSocket

### Connexion
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

### Événements

#### Nouvelle attaque
```javascript
ws.onmessage = function(event) {
    const attack = JSON.parse(event.data);
    console.log('Nouvelle attaque:', attack);
};
```

### Format des données
```json
{
    "id": 123,
    "ip_address": "192.168.1.1",
    "port": 22,
    "protocol": "SSH",
    "country": "United States",
    "city": "New York",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## 🗄️ Base de Données

### Modèle Attack

```python
class Attack(Base):
    id = Column(Integer, primary_key=True)
    ip_address = Column(String(45), nullable=False)
    port = Column(Integer, nullable=False)
    protocol = Column(String(10), nullable=False)
    country = Column(String(100))
    city = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    region = Column(String(100))
    timezone = Column(String(50))
    isp = Column(String(200))
    timestamp = Column(DateTime, nullable=False)
    user_agent = Column(Text)
    additional_data = Column(Text)
```

### Scripts Utilitaires

#### Initialisation
```bash
python init_db.py
```

#### Réinitialisation complète
```bash
python init_db.py --reset
```

#### Génération de données de test
```bash
python populate_fake_attacks.py
```

## 🧪 Tests

### Lancer tous les tests
```bash
pytest tests/ -v
```

### Tests spécifiques
```bash
pytest tests/test_api.py::TestAttacksEndpoints::test_get_attacks_with_data -v
```

### Couverture de code
```bash
pytest --cov=. tests/
```

## 🔍 Honeypot

### Fonctionnement

Le honeypot écoute sur un port TCP configuré et :
1. Accepte toutes les connexions entrantes
2. Capture l'IP source et le port ciblé
3. Géolocalise l'adresse IP
4. Enregistre l'attaque en base de données
5. Envoie l'événement via WebSocket

### Configuration

```python
# Dans main.py
honeypot_server = HoneypotServer(
    port=2222,  # Port à surveiller
    on_attack_callback=handle_new_attack
)
```

### Test de connexion

```bash
# Tester la connexion au honeypot
telnet localhost 2222
```

## 🌍 Géolocalisation

### Service GeoIP

Le service utilise l'API gratuite ip-api.com :
- 1000 requêtes gratuites par minute
- Pas de clé API requise
- Cache des résultats pendant 24h

### Configuration

```python
# Dans services/geoip.py
class GeoIPService:
    def __init__(self):
        self.base_url = "http://ip-api.com/json"
        self.cache_duration = timedelta(hours=24)
        self.rate_limit_delay = 0.1  # 100ms entre requêtes
```

### Test du service

```python
from services.geoip import test_geoip_service
import asyncio

asyncio.run(test_geoip_service())
```

## 📊 Monitoring et Logs

### Logs

Les logs sont configurés avec différents niveaux :
- `INFO` : Informations générales
- `WARNING` : Avertissements
- `ERROR` : Erreurs
- `DEBUG` : Informations de débogage

### Métriques

L'API expose des métriques via `/stats` :
- Nombre total d'attaques
- Attaques des dernières 24h
- Top pays et ports
- Connexions WebSocket actives

### Health Check

```bash
curl http://localhost:8000/health
```

## 🐛 Dépannage

### Problèmes Courants

#### Le honeypot ne démarre pas
```bash
# Vérifier que le port n'est pas utilisé
netstat -tulpn | grep :2222

# Changer le port dans main.py
```

#### Erreur de base de données
```bash
# Réinitialiser la base de données
python init_db.py --reset
```

#### Erreur de géolocalisation
```bash
# Vérifier la connectivité
curl "http://ip-api.com/json/8.8.8.8"
```

#### WebSocket ne fonctionne pas
```bash
# Vérifier les logs
tail -f logs/app.log
```

### Logs

```bash
# Logs en temps réel
python main.py

# Logs avec niveau DEBUG
LOG_LEVEL=DEBUG python main.py
```

## 🔒 Sécurité

### ⚠️ Avertissements

- **Ne pas déployer en production** sans sécurisation appropriée
- **Utiliser uniquement dans des environnements isolés**
- **Les données sont stockées localement** (SQLite)
- **Aucune authentification** implémentée

### Recommandations

1. **Isoler le réseau** : Utiliser un réseau isolé pour le honeypot
2. **Surveiller les logs** : Surveiller les tentatives d'attaque
3. **Sauvegarder les données** : Sauvegarder régulièrement la base de données
4. **Mettre à jour** : Maintenir les dépendances à jour

## 📈 Performance

### Optimisations

- **Cache de géolocalisation** : Évite les appels API répétés
- **Index de base de données** : Requêtes optimisées
- **Pagination** : Limite des résultats
- **WebSocket asynchrone** : Mises à jour en temps réel efficaces

### Limites

- **SQLite** : Limité à un seul processus
- **Géolocalisation** : 1000 req/min max
- **Mémoire** : Cache des connexions WebSocket

## 🤝 Contribution

### Structure du Code

- **Modèles** : `models.py`
- **Routes** : `routes/attacks.py`
- **Services** : `services/geoip.py`
- **Tests** : `tests/test_api.py`

### Ajout de Fonctionnalités

1. Créer une branche feature
2. Implémenter la fonctionnalité
3. Ajouter les tests
4. Mettre à jour la documentation
5. Créer une Pull Request

## 📝 Changelog

### Version 1.0.0
- Honeypot TCP basique
- API REST complète
- WebSocket temps réel
- Géolocalisation IP
- Base de données SQLite
- Tests unitaires
- Documentation complète

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Consulter la documentation API : http://localhost:8000/docs
- Vérifier les logs de l'application

---

**⚡ Développé avec FastAPI, SQLAlchemy et Python pour la cybersécurité**
