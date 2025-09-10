#!/usr/bin/env python3
"""
Honeypot Attack Map - Générateur de fausses attaques
Script pour peupler la base de données avec des données de test
"""

import sys
import os
import random
import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, init_database
from models import Attack
from services.geoip import GeoIPService

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Données de test pour les pays
DEMO_COUNTRIES = [
    {"name": "United States", "lat": 39.8283, "lon": -98.5795, "weight": 25},
    {"name": "China", "lat": 35.8617, "lon": 104.1954, "weight": 20},
    {"name": "Russia", "lat": 61.5240, "lon": 105.3188, "weight": 15},
    {"name": "Germany", "lat": 51.1657, "lon": 10.4515, "weight": 10},
    {"name": "United Kingdom", "lat": 55.3781, "lon": -3.4360, "weight": 8},
    {"name": "France", "lat": 46.2276, "lon": 2.2137, "weight": 7},
    {"name": "Japan", "lat": 36.2048, "lon": 138.2529, "weight": 6},
    {"name": "Brazil", "lat": -14.2350, "lon": -51.9253, "weight": 5},
    {"name": "India", "lat": 20.5937, "lon": 78.9629, "weight": 4},
    {"name": "Canada", "lat": 56.1304, "lon": -106.3468, "weight": 3},
    {"name": "Australia", "lat": -25.2744, "lon": 133.7751, "weight": 2},
    {"name": "South Korea", "lat": 35.9078, "lon": 127.7669, "weight": 2},
    {"name": "Italy", "lat": 41.8719, "lon": 12.5674, "weight": 2},
    {"name": "Spain", "lat": 40.4637, "lon": -3.7492, "weight": 2},
    {"name": "Netherlands", "lat": 52.1326, "lon": 5.2913, "weight": 1},
    {"name": "Poland", "lat": 51.9194, "lon": 19.1451, "weight": 1},
    {"name": "Ukraine", "lat": 48.3794, "lon": 31.1656, "weight": 1},
    {"name": "Turkey", "lat": 38.9637, "lon": 35.2433, "weight": 1},
    {"name": "Iran", "lat": 32.4279, "lon": 53.6880, "weight": 1},
    {"name": "Israel", "lat": 31.0461, "lon": 34.8516, "weight": 1}
]

# Ports communément attaqués avec leurs poids
ATTACK_PORTS = [
    {"port": 22, "protocol": "SSH", "weight": 30, "risk": "CRITICAL"},
    {"port": 80, "protocol": "HTTP", "weight": 25, "risk": "HIGH"},
    {"port": 443, "protocol": "HTTPS", "weight": 20, "risk": "HIGH"},
    {"port": 3389, "protocol": "RDP", "weight": 15, "risk": "CRITICAL"},
    {"port": 5432, "protocol": "PostgreSQL", "weight": 10, "risk": "CRITICAL"},
    {"port": 3306, "protocol": "MySQL", "weight": 10, "risk": "CRITICAL"},
    {"port": 21, "protocol": "FTP", "weight": 8, "risk": "HIGH"},
    {"port": 23, "protocol": "Telnet", "weight": 7, "risk": "HIGH"},
    {"port": 25, "protocol": "SMTP", "weight": 6, "risk": "MEDIUM"},
    {"port": 53, "protocol": "DNS", "weight": 5, "risk": "MEDIUM"},
    {"port": 110, "protocol": "POP3", "weight": 4, "risk": "MEDIUM"},
    {"port": 143, "protocol": "IMAP", "weight": 4, "risk": "MEDIUM"},
    {"port": 993, "protocol": "IMAPS", "weight": 3, "risk": "MEDIUM"},
    {"port": 995, "protocol": "POP3S", "weight": 3, "risk": "MEDIUM"},
    {"port": 587, "protocol": "SMTP", "weight": 2, "risk": "MEDIUM"},
    {"port": 465, "protocol": "SMTPS", "weight": 2, "risk": "MEDIUM"}
]

class FakeAttackGenerator:
    """Générateur de fausses attaques pour les tests"""
    
    def __init__(self):
        self.geoip_service = GeoIPService()
        self.generated_ips = set()
    
    def generate_ip_address(self) -> str:
        """Génère une adresse IP aléatoire"""
        # Générer des IPs dans différentes plages pour plus de réalisme
        first_octet = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255],
            weights=[1] * 255
        )[0]
        
        second_octet = random.randint(0, 255)
        third_octet = random.randint(0, 255)
        fourth_octet = random.randint(1, 254)
        
        ip = f"{first_octet}.{second_octet}.{third_octet}.{fourth_octet}"
        
        # Éviter les doublons
        if ip in self.generated_ips:
            return self.generate_ip_address()
        
        self.generated_ips.add(ip)
        return ip
    
    def select_country(self) -> Dict[str, Any]:
        """Sélectionne un pays aléatoire basé sur les poids"""
        countries = [c["name"] for c in DEMO_COUNTRIES]
        weights = [c["weight"] for c in DEMO_COUNTRIES]
        
        selected_country = random.choices(countries, weights=weights)[0]
        return next(c for c in DEMO_COUNTRIES if c["name"] == selected_country)
    
    def select_port(self) -> Dict[str, Any]:
        """Sélectionne un port aléatoire basé sur les poids"""
        ports = [p["port"] for p in ATTACK_PORTS]
        weights = [p["weight"] for p in ATTACK_PORTS]
        
        selected_port = random.choices(ports, weights=weights)[0]
        return next(p for p in ATTACK_PORTS if p["port"] == selected_port)
    
    def generate_timestamp(self, days_back: int = 7) -> datetime:
        """Génère un timestamp aléatoire dans les derniers jours"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_back)
        
        random_seconds = random.randint(0, int((end_time - start_time).total_seconds()))
        return start_time + timedelta(seconds=random_seconds)
    
    async def create_fake_attack(self, db) -> Attack:
        """Crée une fausse attaque"""
        # Générer les données de base
        ip_address = self.generate_ip_address()
        country_data = self.select_country()
        port_data = self.select_port()
        timestamp = self.generate_timestamp()
        
        # Ajouter de la variation géographique
        lat_offset = random.uniform(-2, 2)
        lon_offset = random.uniform(-2, 2)
        
        # Créer l'attaque
        attack = Attack(
            ip_address=ip_address,
            port=port_data["port"],
            protocol=port_data["protocol"],
            country=country_data["name"],
            city=f"City {random.randint(1, 100)}",
            latitude=country_data["lat"] + lat_offset,
            longitude=country_data["lon"] + lon_offset,
            region=f"Region {random.randint(1, 20)}",
            timezone="UTC",
            isp=f"ISP {random.randint(1, 50)}",
            timestamp=timestamp,
            user_agent=f"User-Agent-{random.randint(1, 1000)}" if random.random() < 0.3 else None,
            additional_data=f'{{"risk_level": "{port_data["risk"]}", "generated": true}}'
        )
        
        return attack
    
    async def generate_attacks(self, count: int, db) -> List[Attack]:
        """Génère un nombre spécifique d'attaques"""
        attacks = []
        
        print(f"🎭 Génération de {count} fausses attaques...")
        
        for i in range(count):
            try:
                attack = await self.create_fake_attack(db)
                attacks.append(attack)
                
                if (i + 1) % 50 == 0:
                    print(f"   Généré {i + 1}/{count} attaques...")
                    
            except Exception as e:
                logger.error(f"Erreur lors de la génération de l'attaque {i + 1}: {e}")
        
        return attacks

async def main():
    """Fonction principale"""
    print("🎭 Générateur de fausses attaques pour Honeypot Attack Map")
    print("=" * 60)
    
    try:
        # Initialiser la base de données
        print("🔧 Initialisation de la base de données...")
        init_database()
        print("✅ Base de données initialisée")
        
        # Obtenir une session de base de données
        db = next(get_db())
        
        try:
            # Créer le générateur
            generator = FakeAttackGenerator()
            
            # Générer les attaques
            print("\n🎭 Génération des attaques...")
            
            # Attaques historiques (derniers 7 jours)
            historical_count = 200
            print(f"📅 Génération de {historical_count} attaques historiques...")
            historical_attacks = await generator.generate_attacks(historical_count, db)
            
            # Attaques récentes (dernières 24h)
            recent_count = 50
            print(f"🔥 Génération de {recent_count} attaques récentes...")
            recent_generator = FakeAttackGenerator()
            recent_generator.generate_timestamp = lambda: datetime.now() - timedelta(hours=random.randint(0, 24))
            recent_attacks = await recent_generator.generate_attacks(recent_count, db)
            
            # Sauvegarder en base de données
            print("\n💾 Sauvegarde en base de données...")
            
            all_attacks = historical_attacks + recent_attacks
            
            for attack in all_attacks:
                db.add(attack)
            
            db.commit()
            
            print(f"✅ {len(all_attacks)} attaques sauvegardées avec succès!")
            
            # Afficher les statistiques
            print("\n📊 Statistiques générées:")
            total_attacks = db.query(Attack).count()
            recent_24h = db.query(Attack).filter(Attack.timestamp >= datetime.now() - timedelta(days=1)).count()
            
            print(f"   Total d'attaques: {total_attacks}")
            print(f"   Attaques 24h: {recent_24h}")
            
            # Top pays
            from sqlalchemy import func
            top_countries = db.query(
                Attack.country,
                func.count(Attack.id).label('count')
            ).group_by(Attack.country).order_by(func.count(Attack.id).desc()).limit(5).all()
            
            print("   Top 5 pays:")
            for country, count in top_countries:
                print(f"     {country}: {count}")
            
            # Top ports
            top_ports = db.query(
                Attack.port,
                func.count(Attack.id).label('count')
            ).group_by(Attack.port).order_by(func.count(Attack.id).desc()).limit(5).all()
            
            print("   Top 5 ports:")
            for port, count in top_ports:
                print(f"     {port}: {count}")
            
            print("\n🎉 Génération terminée avec succès!")
            print("\n📝 Prochaines étapes:")
            print("   1. Lancer le serveur: python main.py")
            print("   2. Accéder à l'API: http://localhost:8000/docs")
            print("   3. Voir les attaques: http://localhost:8000/api/attacks")
            
        finally:
            db.close()
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la génération: {e}")
        print(f"\n❌ Erreur: {e}")
        return 1

def show_help():
    """Affiche l'aide du script"""
    print("""
🎭 Générateur de fausses attaques

Usage:
    python populate_fake_attacks.py

Description:
    Ce script génère des fausses attaques pour tester l'application
    sans avoir besoin de vraies tentatives d'intrusion.

    Il génère:
    - 200 attaques historiques (derniers 7 jours)
    - 50 attaques récentes (dernières 24h)
    - Données géolocalisées réalistes
    - Ports et protocoles variés

Exemples:
    # Génération normale
    python populate_fake_attacks.py
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_help()
        sys.exit(0)
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
