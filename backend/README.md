# 🗄️ Honeypot Attack Map - Base de Données

Configuration et modèles de base de données pour le système de visualisation d'attaques en temps réel.

## 🎯 Vue d'ensemble

Ce module fournit :
- **Configuration SQLAlchemy** pour SQLite (dev) et PostgreSQL (prod)
- **Modèle Attack** complet avec géolocalisation
- **Scripts d'initialisation** et de gestion
- **Générateur de données de test** pour les démonstrations

## 🏗️ Architecture

```
backend/
├── database.py              # Configuration SQLAlchemy
├── models.py                # Modèles de données
├── init_db.py              # Script d'initialisation
├── populate_fake_attacks.py # Générateur de données de test
├── example_usage.py        # Exemples d'utilisation
└── README.md               # Cette documentation
```

## 🚀 Installation et Initialisation

### Prérequis
- Python 3.11+
- SQLAlchemy
- SQLite3 (inclus avec Python)

### Installation

1. **Installer les dépendances**
```bash
pip install sqlalchemy
```

2. **Initialiser la base de données**
```bash
python init_db.py
```

3. **Générer des données de test (optionnel)**
```bash
python populate_fake_attacks.py
```

4. **Tester avec des exemples**
```bash
python example_usage.py
```

## 📊 Modèle de Données

### Table `attacks`

| Champ | Type | Description |
|-------|------|-------------|
| `id` | Integer | Clé primaire auto-incrémentée |
| `ip_address` | String(45) | Adresse IP de l'attaquant |
| `port` | Integer | Port ciblé par l'attaque |
| `protocol` | String(10) | Protocole utilisé (TCP, UDP, etc.) |
| `country` | String(100) | Pays d'origine |
| `city` | String(100) | Ville d'origine |
| `latitude` | Float | Latitude géographique |
| `longitude` | Float | Longitude géographique |
| `region` | String(100) | Région/État |
| `timezone` | String(50) | Fuseau horaire |
| `isp` | String(200) | Fournisseur d'accès internet |
| `timestamp` | DateTime | Horodatage de l'attaque |
| `user_agent` | Text | User-Agent si disponible |
| `additional_data` | Text | Données supplémentaires (JSON) |

### Index de Performance

- `idx_ip_address` : Index sur l'adresse IP
- `idx_timestamp` : Index sur l'horodatage
- `idx_country` : Index sur le pays
- `idx_ip_timestamp` : Index composé IP + timestamp
- `idx_country_timestamp` : Index composé pays + timestamp
- `idx_port_timestamp` : Index composé port + timestamp

## 🔧 Configuration

### Variables d'environnement

```env
DATABASE_URL=sqlite:///./honeypot_attacks.db
```

### Configuration SQLite (Développement)

```python
# Dans database.py
engine = create_engine(
    "sqlite:///./honeypot_attacks.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)
```

### Configuration PostgreSQL (Production)

```python
# Dans database.py
engine = create_engine(
    "postgresql://user:password@localhost/honeypot",
    echo=False,
    pool_pre_ping=True
)
```

## 📝 Utilisation

### Création d'une attaque

```python
from database import get_db
from models import Attack
from datetime import datetime

# Créer une attaque
attack = Attack(
    ip_address="192.168.1.100",
    port=22,
    protocol="SSH",
    country="United States",
    city="New York",
    latitude=40.7128,
    longitude=-74.0060,
    timestamp=datetime.now()
)

# Sauvegarder
db = next(get_db())
db.add(attack)
db.commit()
db.close()
```

### Requêtes de base

```python
from database import get_db
from models import Attack
from sqlalchemy import func

db = next(get_db())

# Toutes les attaques
attacks = db.query(Attack).all()

# Attaques récentes (24h)
from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(days=1)
recent = db.query(Attack).filter(Attack.timestamp >= yesterday).all()

# Statistiques par pays
country_stats = db.query(
    Attack.country,
    func.count(Attack.id).label('count')
).group_by(Attack.country).all()

db.close()
```

### Requêtes avancées

```python
from sqlalchemy import and_, or_, func

# Attaques critiques (SSH, RDP, etc.)
critical_ports = [22, 3389, 5432, 3306]
critical = db.query(Attack).filter(Attack.port.in_(critical_ports)).all()

# Attaques géolocalisées
geo_attacks = db.query(Attack).filter(
    and_(
        Attack.latitude.isnot(None),
        Attack.longitude.isnot(None)
    )
).all()

# Attaques par heure
hourly = db.query(
    func.extract('hour', Attack.timestamp).label('hour'),
    func.count(Attack.id).label('count')
).group_by('hour').all()
```

## 🛠️ Scripts Utilitaires

### `init_db.py`

Script d'initialisation de la base de données.

```bash
# Initialisation normale
python init_db.py

# Réinitialisation complète (ATTENTION: supprime toutes les données!)
python init_db.py --reset

# Aide
python init_db.py --help
```

### `populate_fake_attacks.py`

Générateur de données de test.

```bash
# Générer des données de test
python populate_fake_attacks.py

# Aide
python populate_fake_attacks.py --help
```

**Données générées :**
- 200 attaques historiques (derniers 7 jours)
- 50 attaques récentes (dernières 24h)
- 20 pays différents avec poids réalistes
- 16 ports communément attaqués
- Géolocalisation réaliste

### `example_usage.py`

Exemples d'utilisation des modèles.

```bash
# Lancer les exemples
python example_usage.py
```

## 📊 Fonctions Utilitaires

### `database.py`

```python
# Vérifier la connexion
check_database_connection()

# Obtenir des informations
get_database_info()

# Statistiques des tables
get_table_stats()

# Taille de la base de données
get_database_size()
```

### `models.py`

```python
# Conversion en dictionnaire
attack.to_dict()

# Conversion pour WebSocket
attack.to_websocket_dict()

# Vérifier si récent
attack.is_recent(hours=24)

# Obtenir la localisation
attack.get_location_string()

# Niveau de risque
attack.get_risk_level()
```

## 🔍 Requêtes de Performance

### Requêtes optimisées

```python
# Pagination efficace
attacks = db.query(Attack).order_by(Attack.timestamp.desc()).offset(0).limit(100).all()

# Filtrage par index
us_attacks = db.query(Attack).filter(Attack.country == "United States").all()

# Requêtes composées
recent_us_attacks = db.query(Attack).filter(
    and_(
        Attack.country == "United States",
        Attack.timestamp >= yesterday
    )
).all()
```

### Index recommandés

```python
# Index sur les champs fréquemment utilisés
Index('idx_ip_address', 'ip_address')
Index('idx_timestamp', 'timestamp')
Index('idx_country', 'country')

# Index composés pour les requêtes complexes
Index('idx_ip_timestamp', 'ip_address', 'timestamp')
Index('idx_country_timestamp', 'country', 'timestamp')
```

## 🧪 Tests

### Tests de base

```python
# Test de connexion
from database import check_database_connection
assert check_database_connection() == True

# Test de création
attack = Attack(ip_address="1.1.1.1", port=80, protocol="HTTP")
db.add(attack)
db.commit()
assert attack.id is not None
```

### Tests de performance

```python
import time

# Test de requête simple
start = time.time()
attacks = db.query(Attack).all()
duration = time.time() - start
print(f"Requête simple: {duration:.3f}s pour {len(attacks)} attaques")
```

## 🔒 Sécurité

### Bonnes pratiques

1. **Validation des données** : Valider les entrées avant insertion
2. **Requêtes paramétrées** : Utiliser les paramètres SQLAlchemy
3. **Gestion des erreurs** : Capturer et logger les erreurs
4. **Sauvegardes** : Sauvegarder régulièrement la base de données

### Exemple de validation

```python
def validate_attack_data(data):
    """Valide les données d'une attaque"""
    if not data.get('ip_address'):
        raise ValueError("IP address is required")
    
    if not isinstance(data.get('port'), int) or not (1 <= data.get('port') <= 65535):
        raise ValueError("Port must be an integer between 1 and 65535")
    
    return True
```

## 📈 Monitoring

### Métriques importantes

```python
# Nombre total d'attaques
total_attacks = db.query(Attack).count()

# Taux d'attaques par heure
hourly_rate = db.query(
    func.extract('hour', Attack.timestamp).label('hour'),
    func.count(Attack.id).label('count')
).group_by('hour').all()

# Top pays attaquants
top_countries = db.query(
    Attack.country,
    func.count(Attack.id).label('count')
).group_by(Attack.country).order_by(func.count(Attack.id).desc()).limit(10).all()
```

### Logs de performance

```python
import logging

# Logger les requêtes lentes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)
```

## 🐛 Dépannage

### Problèmes courants

#### Erreur de connexion SQLite
```bash
# Vérifier les permissions
ls -la honeypot_attacks.db

# Réinitialiser la base
python init_db.py --reset
```

#### Erreur de threading SQLite
```python
# Utiliser StaticPool
engine = create_engine(
    "sqlite:///./honeypot_attacks.db",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False}
)
```

#### Requêtes lentes
```python
# Ajouter des index
from sqlalchemy import Index
Index('idx_timestamp', Attack.timestamp)
Index('idx_country', Attack.country)
```

### Logs de débogage

```python
# Activer les logs SQL
engine = create_engine("sqlite:///./honeypot_attacks.db", echo=True)
```

## 📚 Ressources

### Documentation SQLAlchemy
- [SQLAlchemy Core](https://docs.sqlalchemy.org/en/14/core/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [SQLAlchemy Engine](https://docs.sqlalchemy.org/en/14/core/engines.html)

### Documentation SQLite
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [SQLite Data Types](https://www.sqlite.org/datatype3.html)

### Outils de gestion
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [SQLite Studio](https://sqlitestudio.pl/)

---

**⚡ Développé avec SQLAlchemy et Python pour la cybersécurité**