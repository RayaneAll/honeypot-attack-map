"""
Honeypot Attack Map - Main FastAPI Application
Point d'entrée principal de l'API backend
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import threading
from datetime import datetime
from typing import List, Dict, Any
import logging

from database import engine, Base, get_db
from models import Attack
from routes.attacks import router as attacks_router
from services.geoip import GeoIPService
from honeypot import HoneypotServer

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title="Honeypot Attack Map API",
    description="API pour visualiser les attaques détectées par le honeypot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(attacks_router, prefix="/api", tags=["attacks"])

# Service de géolocalisation
geoip_service = GeoIPService()

# Serveur honeypot
honeypot_server = None

# Gestionnaire des connexions WebSocket
class ConnectionManager:
    """Gestionnaire des connexions WebSocket pour le temps réel"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """Accepter une nouvelle connexion WebSocket"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connecté. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Déconnecter un WebSocket"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket déconnecté. Total: {len(self.active_connections)}")
    
    async def send_attack(self, attack_data: Dict[str, Any]):
        """Envoyer une nouvelle attaque à tous les clients connectés"""
        if self.active_connections:
            # Créer une copie de la liste pour éviter les modifications pendant l'itération
            connections = self.active_connections.copy()
            for connection in connections:
                try:
                    await connection.send_json(attack_data)
                except Exception as e:
                    logger.error(f"Erreur envoi WebSocket: {e}")
                    self.disconnect(connection)

# Instance globale du gestionnaire de connexions
manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    """Événement de démarrage de l'application"""
    logger.info("🚀 Démarrage de l'API Honeypot Attack Map...")
    
    # Créer les tables de base de données
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Base de données initialisée")
    
    # Démarrer le serveur honeypot
    global honeypot_server
    honeypot_server = HoneypotServer(
        port=2222,
        on_attack_callback=handle_new_attack
    )
    
    # Démarrer le honeypot dans un thread séparé
    honeypot_thread = threading.Thread(target=honeypot_server.start, daemon=True)
    honeypot_thread.start()
    logger.info("🔥 Honeypot démarré sur le port 2222")

@app.on_event("shutdown")
async def shutdown_event():
    """Événement d'arrêt de l'application"""
    logger.info("🛑 Arrêt de l'API Honeypot Attack Map...")
    
    if honeypot_server:
        honeypot_server.stop()
        logger.info("✅ Honeypot arrêté")

async def handle_new_attack(ip_address: str, port: int, protocol: str = "TCP"):
    """
    Gestionnaire appelé lorsqu'une nouvelle attaque est détectée
    
    Args:
        ip_address (str): Adresse IP de l'attaquant
        port (int): Port ciblé
        protocol (str): Protocole utilisé
    """
    try:
        logger.info(f"🚨 Nouvelle attaque détectée: {ip_address}:{port} ({protocol})")
        
        # Géolocaliser l'IP
        location = await geoip_service.get_location(ip_address)
        
        # Créer l'objet attaque
        attack = Attack(
            ip_address=ip_address,
            port=port,
            protocol=protocol,
            country=location.get('country', 'Unknown'),
            city=location.get('city', 'Unknown'),
            latitude=location.get('latitude', 0.0),
            longitude=location.get('longitude', 0.0),
            timestamp=datetime.now()
        )
        
        # Sauvegarder en base de données
        db = next(get_db())
        try:
            db.add(attack)
            db.commit()
            db.refresh(attack)
            logger.info(f"✅ Attaque sauvegardée avec l'ID: {attack.id}")
        finally:
            db.close()
        
        # Préparer les données pour le WebSocket
        attack_data = {
            "id": attack.id,
            "ip_address": attack.ip_address,
            "port": attack.port,
            "protocol": attack.protocol,
            "country": attack.country,
            "city": attack.city,
            "latitude": attack.latitude,
            "longitude": attack.longitude,
            "timestamp": attack.timestamp.isoformat()
        }
        
        # Envoyer via WebSocket
        await manager.send_attack(attack_data)
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement de l'attaque: {e}")

@app.get("/")
async def root():
    """Endpoint racine avec informations sur l'API"""
    return {
        "message": "Honeypot Attack Map API",
        "version": "1.0.0",
        "status": "running",
        "honeypot_port": 2222,
        "websocket_url": "/ws",
        "docs_url": "/docs"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de santé de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "honeypot_running": honeypot_server is not None,
        "websocket_connections": len(manager.active_connections)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Endpoint WebSocket pour recevoir les attaques en temps réel
    
    Le client peut se connecter à ws://localhost:8000/ws
    pour recevoir les nouvelles attaques instantanément
    """
    await manager.connect(websocket)
    try:
        while True:
            # Maintenir la connexion active
            data = await websocket.receive_text()
            logger.debug(f"Message reçu du client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client WebSocket déconnecté")

@app.get("/stats")
async def get_stats():
    """Statistiques générales des attaques"""
    db = next(get_db())
    try:
        # Compter le total d'attaques
        total_attacks = db.query(Attack).count()
        
        # Compter les attaques des dernières 24h
        from datetime import datetime, timedelta
        yesterday = datetime.now() - timedelta(days=1)
        recent_attacks = db.query(Attack).filter(Attack.timestamp >= yesterday).count()
        
        # Top 5 des pays
        from sqlalchemy import func
        top_countries = db.query(
            Attack.country,
            func.count(Attack.id).label('count')
        ).group_by(Attack.country).order_by(func.count(Attack.id).desc()).limit(5).all()
        
        # Top 5 des ports
        top_ports = db.query(
            Attack.port,
            func.count(Attack.id).label('count')
        ).group_by(Attack.port).order_by(func.count(Attack.id).desc()).limit(5).all()
        
        return {
            "total_attacks": total_attacks,
            "recent_attacks_24h": recent_attacks,
            "top_countries": [{"country": country, "count": count} for country, count in top_countries],
            "top_ports": [{"port": port, "count": count} for port, count in top_ports],
            "websocket_connections": len(manager.active_connections)
        }
    finally:
        db.close()

if __name__ == "__main__":
    # Configuration pour le développement
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
