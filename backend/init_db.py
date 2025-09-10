#!/usr/bin/env python3
"""
Honeypot Attack Map - Script d'initialisation de la base de données
Script pour créer et initialiser la base de données SQLite
"""

import sys
import os
import logging
from datetime import datetime

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_database, check_database_connection, get_database_info, get_table_stats
from models import Attack, AttackStats

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Fonction principale d'initialisation"""
    print("🗄️  Initialisation de la base de données Honeypot Attack Map")
    print("=" * 60)
    
    try:
        # Vérifier la connexion à la base de données
        print("🔍 Vérification de la connexion à la base de données...")
        if not check_database_connection():
            print("❌ Impossible de se connecter à la base de données")
            return 1
        
        print("✅ Connexion à la base de données OK")
        
        # Afficher les informations sur la base de données
        print("\n📊 Informations sur la base de données:")
        info = get_database_info()
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Initialiser la base de données
        print("\n🔧 Initialisation des tables...")
        init_database()
        print("✅ Tables créées avec succès")
        
        # Vérifier les statistiques
        print("\n📈 Statistiques de la base de données:")
        stats = get_table_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print("\n🎉 Initialisation terminée avec succès!")
        print("\n📝 Prochaines étapes:")
        print("   1. Lancer le serveur: python main.py")
        print("   2. Générer des données de test: python populate_fake_attacks.py")
        print("   3. Accéder à l'API: http://localhost:8000/docs")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'initialisation: {e}")
        print(f"\n❌ Erreur: {e}")
        return 1

def reset_database():
    """Réinitialise complètement la base de données"""
    print("🔄 Réinitialisation de la base de données...")
    
    try:
        from database import reset_database
        reset_database()
        print("✅ Base de données réinitialisée")
        return 0
    except Exception as e:
        logger.error(f"❌ Erreur lors de la réinitialisation: {e}")
        return 1

def show_help():
    """Affiche l'aide du script"""
    print("""
🗄️  Script d'initialisation de la base de données

Usage:
    python init_db.py              # Initialise la base de données
    python init_db.py --reset      # Réinitialise la base de données
    python init_db.py --help       # Affiche cette aide

Options:
    --reset    Supprime et recrée toutes les tables (ATTENTION: supprime toutes les données!)
    --help     Affiche cette aide

Exemples:
    # Initialisation normale
    python init_db.py
    
    # Réinitialisation complète
    python init_db.py --reset
    """)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            exit_code = reset_database()
        elif sys.argv[1] == "--help":
            show_help()
            exit_code = 0
        else:
            print(f"❌ Option inconnue: {sys.argv[1]}")
            show_help()
            exit_code = 1
    else:
        exit_code = main()
    
    sys.exit(exit_code)
