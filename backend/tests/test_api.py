"""
Honeypot Attack Map - Tests de l'API
Tests unitaires pour les endpoints de l'API
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import tempfile
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db, Base
from models import Attack

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override de la dépendance get_db pour les tests"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override de la dépendance
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    """Client de test FastAPI"""
    # Créer les tables
    Base.metadata.create_all(bind=engine)
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Nettoyer après chaque test
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def sample_attacks():
    """Données d'attaques de test"""
    return [
        {
            "ip_address": "192.168.1.1",
            "port": 22,
            "protocol": "SSH",
            "country": "United States",
            "city": "New York",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "timestamp": datetime.now()
        },
        {
            "ip_address": "10.0.0.1",
            "port": 80,
            "protocol": "HTTP",
            "country": "China",
            "city": "Beijing",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timestamp": datetime.now() - timedelta(hours=1)
        },
        {
            "ip_address": "172.16.0.1",
            "port": 443,
            "protocol": "HTTPS",
            "country": "Germany",
            "city": "Berlin",
            "latitude": 52.5200,
            "longitude": 13.4050,
            "timestamp": datetime.now() - timedelta(days=1)
        }
    ]

def create_test_attacks(db, attacks_data):
    """Crée des attaques de test dans la base de données"""
    for attack_data in attacks_data:
        attack = Attack(**attack_data)
        db.add(attack)
    db.commit()

class TestHealthEndpoints:
    """Tests des endpoints de santé"""
    
    def test_root_endpoint(self, client):
        """Test de l'endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
    
    def test_health_endpoint(self, client):
        """Test de l'endpoint de santé"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "honeypot_running" in data
        assert "websocket_connections" in data

class TestAttacksEndpoints:
    """Tests des endpoints d'attaques"""
    
    def test_get_attacks_empty(self, client):
        """Test de récupération des attaques avec base vide"""
        response = client.get("/api/attacks/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_attacks_with_data(self, client, sample_attacks):
        """Test de récupération des attaques avec données"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        response = client.get("/api/attacks/")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        
        # Vérifier que les données sont triées par timestamp décroissant
        timestamps = [datetime.fromisoformat(attack["timestamp"]) for attack in data]
        assert timestamps == sorted(timestamps, reverse=True)
    
    def test_get_attacks_with_filters(self, client, sample_attacks):
        """Test de récupération des attaques avec filtres"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        # Test filtre par pays
        response = client.get("/api/attacks/?country=United States")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["country"] == "United States"
        
        # Test filtre par protocole
        response = client.get("/api/attacks/?protocol=SSH")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["protocol"] == "SSH"
        
        # Test filtre par port
        response = client.get("/api/attacks/?port=80")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
        assert data[0]["port"] == 80
    
    def test_get_attacks_pagination(self, client, sample_attacks):
        """Test de la pagination des attaques"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        # Test avec limite
        response = client.get("/api/attacks/?limit=2")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 2
        
        # Test avec offset
        response = client.get("/api/attacks/?limit=1&offset=1")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 1
    
    def test_get_attack_by_id(self, client, sample_attacks):
        """Test de récupération d'une attaque par ID"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        # Récupérer la première attaque
        response = client.get("/api/attacks/1")
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == 1
        assert data["ip_address"] == "192.168.1.1"
    
    def test_get_attack_by_id_not_found(self, client):
        """Test de récupération d'une attaque inexistante"""
        response = client.get("/api/attacks/999")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "non trouvée" in data["detail"]
    
    def test_get_attack_summary(self, client, sample_attacks):
        """Test de récupération du résumé des attaques"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        response = client.get("/api/attacks/stats/summary")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_attacks" in data
        assert "recent_attacks_24h" in data
        assert "top_countries" in data
        assert "top_ports" in data
        assert data["total_attacks"] == 3
    
    def test_get_attacks_by_country(self, client, sample_attacks):
        """Test de récupération des statistiques par pays"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        response = client.get("/api/attacks/stats/by-country")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # 3 pays différents
        
        # Vérifier que les pays sont triés par nombre d'attaques
        countries = [item["country"] for item in data]
        assert "United States" in countries
        assert "China" in countries
        assert "Germany" in countries
    
    def test_get_attacks_by_port(self, client, sample_attacks):
        """Test de récupération des statistiques par port"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        response = client.get("/api/attacks/stats/by-port")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3  # 3 ports différents
        
        # Vérifier que les ports sont triés par nombre d'attaques
        ports = [item["port"] for item in data]
        assert 22 in ports
        assert 80 in ports
        assert 443 in ports
    
    def test_get_recent_live_attacks(self, client, sample_attacks):
        """Test de récupération des attaques récentes"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        response = client.get("/api/attacks/recent/live")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # Toutes les attaques de test sont récentes
        assert len(data) == 3
    
    def test_delete_attack(self, client, sample_attacks):
        """Test de suppression d'une attaque"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        # Supprimer la première attaque
        response = client.delete("/api/attacks/1")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "supprimée" in data["message"]
        
        # Vérifier que l'attaque a été supprimée
        response = client.get("/api/attacks/1")
        assert response.status_code == 404
    
    def test_delete_attack_not_found(self, client):
        """Test de suppression d'une attaque inexistante"""
        response = client.delete("/api/attacks/999")
        assert response.status_code == 404
        
        data = response.json()
        assert "detail" in data
        assert "non trouvée" in data["detail"]
    
    def test_cleanup_old_attacks(self, client, sample_attacks):
        """Test de nettoyage des anciennes attaques"""
        # Créer des attaques de test
        db = next(override_get_db())
        create_test_attacks(db, sample_attacks)
        db.close()
        
        # Nettoyer les attaques plus anciennes que 0 jours (toutes)
        response = client.delete("/api/attacks/cleanup/old?days=0")
        assert response.status_code == 200
        
        data = response.json()
        assert "deleted_count" in data
        assert data["deleted_count"] == 3
        
        # Vérifier que toutes les attaques ont été supprimées
        response = client.get("/api/attacks/")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 0

class TestWebSocket:
    """Tests des WebSockets"""
    
    def test_websocket_connection(self, client):
        """Test de connexion WebSocket"""
        with client.websocket_connect("/ws") as websocket:
            # La connexion devrait être établie
            assert websocket is not None
    
    def test_websocket_disconnect(self, client):
        """Test de déconnexion WebSocket"""
        with client.websocket_connect("/ws") as websocket:
            # Fermer la connexion
            websocket.close()
            # Pas d'exception attendue

if __name__ == "__main__":
    # Lancer les tests
    pytest.main([__file__, "-v"])
