#!/usr/bin/env python3
"""
Honeypot Attack Map - Exemple d'utilisation de la base de données
Script de démonstration pour montrer comment utiliser les modèles SQLAlchemy
"""

import sys
import os
from datetime import datetime, timedelta

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import get_db, init_database
from models import Attack

def example_create_attack():
    """Exemple de création d'une attaque"""
    print("🎯 Exemple de création d'une attaque...")
    
    # Créer une attaque factice
    attack = Attack(
        ip_address="192.168.1.100",
        port=22,
        protocol="SSH",
        country="United States",
        city="New York",
        latitude=40.7128,
        longitude=-74.0060,
        region="New York",
        timezone="America/New_York",
        isp="Verizon",
        timestamp=datetime.now(),
        user_agent="SSH-2.0-OpenSSH_8.2p1",
        additional_data='{"risk_level": "CRITICAL", "source": "example"}'
    )
    
    # Sauvegarder en base de données
    db = next(get_db())
    try:
        db.add(attack)
        db.commit()
        db.refresh(attack)
        
        print(f"✅ Attaque créée avec l'ID: {attack.id}")
        print(f"   IP: {attack.ip_address}")
        print(f"   Port: {attack.port}")
        print(f"   Pays: {attack.country}")
        print(f"   Timestamp: {attack.timestamp}")
        
        return attack
    finally:
        db.close()

def example_query_attacks():
    """Exemple de requête des attaques"""
    print("\n🔍 Exemple de requête des attaques...")
    
    db = next(get_db())
    try:
        # Récupérer toutes les attaques
        all_attacks = db.query(Attack).all()
        print(f"📊 Total d'attaques: {len(all_attacks)}")
        
        # Récupérer les attaques récentes (dernières 24h)
        yesterday = datetime.now() - timedelta(days=1)
        recent_attacks = db.query(Attack).filter(Attack.timestamp >= yesterday).all()
        print(f"🔥 Attaques récentes (24h): {len(recent_attacks)}")
        
        # Récupérer les attaques par pays
        us_attacks = db.query(Attack).filter(Attack.country == "United States").all()
        print(f"🇺🇸 Attaques depuis les USA: {len(us_attacks)}")
        
        # Récupérer les attaques par port
        ssh_attacks = db.query(Attack).filter(Attack.port == 22).all()
        print(f"🔐 Attaques SSH (port 22): {len(ssh_attacks)}")
        
        # Afficher les 5 dernières attaques
        print("\n📋 5 dernières attaques:")
        latest_attacks = db.query(Attack).order_by(Attack.timestamp.desc()).limit(5).all()
        for attack in latest_attacks:
            print(f"   {attack.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {attack.ip_address}:{attack.port} ({attack.country})")
        
    finally:
        db.close()

def example_statistics():
    """Exemple de calcul de statistiques"""
    print("\n📈 Exemple de calcul de statistiques...")
    
    db = next(get_db())
    try:
        from sqlalchemy import func
        
        # Statistiques par pays
        print("🌍 Top 5 des pays:")
        country_stats = db.query(
            Attack.country,
            func.count(Attack.id).label('count')
        ).group_by(Attack.country).order_by(func.count(Attack.id).desc()).limit(5).all()
        
        for country, count in country_stats:
            print(f"   {country}: {count} attaques")
        
        # Statistiques par port
        print("\n🔌 Top 5 des ports:")
        port_stats = db.query(
            Attack.port,
            func.count(Attack.id).label('count')
        ).group_by(Attack.port).order_by(func.count(Attack.id).desc()).limit(5).all()
        
        for port, count in port_stats:
            print(f"   Port {port}: {count} attaques")
        
        # Statistiques par protocole
        print("\n📡 Statistiques par protocole:")
        protocol_stats = db.query(
            Attack.protocol,
            func.count(Attack.id).label('count')
        ).group_by(Attack.protocol).order_by(func.count(Attack.id).desc()).all()
        
        for protocol, count in protocol_stats:
            print(f"   {protocol}: {count} attaques")
        
    finally:
        db.close()

def example_update_attack():
    """Exemple de mise à jour d'une attaque"""
    print("\n✏️ Exemple de mise à jour d'une attaque...")
    
    db = next(get_db())
    try:
        # Récupérer la première attaque
        attack = db.query(Attack).first()
        if attack:
            print(f"📝 Mise à jour de l'attaque ID {attack.id}")
            
            # Mettre à jour des champs
            attack.isp = "Updated ISP"
            attack.additional_data = '{"updated": true, "risk_level": "HIGH"}'
            
            # Sauvegarder les changements
            db.commit()
            
            print("✅ Attaque mise à jour avec succès")
        else:
            print("❌ Aucune attaque trouvée")
    finally:
        db.close()

def example_delete_attack():
    """Exemple de suppression d'une attaque"""
    print("\n🗑️ Exemple de suppression d'une attaque...")
    
    db = next(get_db())
    try:
        # Récupérer la première attaque
        attack = db.query(Attack).first()
        if attack:
            print(f"🗑️ Suppression de l'attaque ID {attack.id}")
            
            # Supprimer l'attaque
            db.delete(attack)
            db.commit()
            
            print("✅ Attaque supprimée avec succès")
        else:
            print("❌ Aucune attaque trouvée")
    finally:
        db.close()

def example_advanced_queries():
    """Exemple de requêtes avancées"""
    print("\n🔬 Exemple de requêtes avancées...")
    
    db = next(get_db())
    try:
        from sqlalchemy import and_, or_, func
        
        # Attaques critiques (SSH, RDP, etc.)
        critical_ports = [22, 3389, 5432, 3306]
        critical_attacks = db.query(Attack).filter(Attack.port.in_(critical_ports)).all()
        print(f"🚨 Attaques critiques: {len(critical_attacks)}")
        
        # Attaques depuis des pays spécifiques
        target_countries = ["United States", "China", "Russia"]
        targeted_attacks = db.query(Attack).filter(Attack.country.in_(target_countries)).all()
        print(f"🎯 Attaques depuis pays ciblés: {len(targeted_attacks)}")
        
        # Attaques avec géolocalisation complète
        geo_attacks = db.query(Attack).filter(
            and_(
                Attack.latitude.isnot(None),
                Attack.longitude.isnot(None),
                Attack.latitude != 0,
                Attack.longitude != 0
            )
        ).all()
        print(f"🌍 Attaques géolocalisées: {len(geo_attacks)}")
        
        # Attaques par heure de la journée
        print("\n⏰ Attaques par heure de la journée:")
        hourly_stats = db.query(
            func.extract('hour', Attack.timestamp).label('hour'),
            func.count(Attack.id).label('count')
        ).group_by('hour').order_by('hour').all()
        
        for hour, count in hourly_stats:
            print(f"   {int(hour):02d}:00 - {count} attaques")
        
    finally:
        db.close()

def main():
    """Fonction principale de démonstration"""
    print("🎭 Exemple d'utilisation de la base de données Honeypot Attack Map")
    print("=" * 70)
    
    try:
        # Initialiser la base de données
        print("🔧 Initialisation de la base de données...")
        init_database()
        print("✅ Base de données initialisée")
        
        # Exemples d'utilisation
        example_create_attack()
        example_query_attacks()
        example_statistics()
        example_update_attack()
        example_delete_attack()
        example_advanced_queries()
        
        print("\n🎉 Tous les exemples ont été exécutés avec succès!")
        print("\n📝 Prochaines étapes:")
        print("   1. Explorer l'API: python main.py")
        print("   2. Générer plus de données: python populate_fake_attacks.py")
        print("   3. Consulter la documentation: README.md")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution des exemples: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
