"""
Honeypot Attack Map - Configuration Base de Données
Configuration SQLAlchemy pour la base de données SQLite
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./honeypot_attacks.db")

# Configuration spéciale pour SQLite
if DATABASE_URL.startswith("sqlite"):
    # Utiliser StaticPool pour éviter les problèmes de threading avec SQLite
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Mettre à True pour voir les requêtes SQL
    )
else:
    # Configuration pour PostgreSQL ou autres bases de données
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True  # Vérifier la connexion avant utilisation
    )

# Factory pour créer les sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Générateur de sessions de base de données
    
    Cette fonction est utilisée comme dépendance FastAPI
    pour obtenir une session de base de données.
    
    Yields:
        Session: Session SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    """
    Initialise la base de données en créant toutes les tables
    
    Cette fonction doit être appelée au démarrage de l'application
    pour s'assurer que toutes les tables existent.
    """
    try:
        # Importer tous les modèles pour qu'ils soient enregistrés
        from models import Attack, AttackStats
        
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        print("✅ Base de données initialisée avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
        raise

def drop_database():
    """
    Supprime toutes les tables de la base de données
    
    ⚠️ ATTENTION: Cette fonction supprime toutes les données!
    """
    try:
        Base.metadata.drop_all(bind=engine)
        print("🗑️ Toutes les tables ont été supprimées")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des tables: {e}")
        raise

def reset_database():
    """
    Réinitialise complètement la base de données
    
    ⚠️ ATTENTION: Cette fonction supprime toutes les données!
    """
    print("🔄 Réinitialisation de la base de données...")
    drop_database()
    init_database()
    print("✅ Base de données réinitialisée")

def get_database_info() -> dict:
    """
    Retourne des informations sur la base de données
    
    Returns:
        dict: Informations sur la configuration de la base de données
    """
    return {
        "database_url": DATABASE_URL,
        "engine_name": engine.name,
        "pool_size": engine.pool.size(),
        "checked_out_connections": engine.pool.checkedout(),
        "overflow_connections": engine.pool.overflow(),
        "tables": list(Base.metadata.tables.keys())
    }

def check_database_connection() -> bool:
    """
    Vérifie si la connexion à la base de données fonctionne
    
    Returns:
        bool: True si la connexion est OK
    """
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def get_table_stats() -> dict:
    """
    Retourne des statistiques sur les tables de la base de données
    
    Returns:
        dict: Statistiques des tables
    """
    stats = {}
    
    try:
        db = next(get_db())
        
        # Compter les attaques
        from models import Attack
        total_attacks = db.query(Attack).count()
        
        # Compter les attaques récentes (24h)
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_attacks = db.query(Attack).filter(Attack.timestamp >= yesterday).count()
        
        # Compter les pays uniques
        unique_countries = db.query(Attack.country).distinct().count()
        
        # Compter les IPs uniques
        unique_ips = db.query(Attack.ip_address).distinct().count()
        
        stats = {
            "total_attacks": total_attacks,
            "recent_attacks_24h": recent_attacks,
            "unique_countries": unique_countries,
            "unique_ips": unique_ips,
            "database_size_mb": get_database_size()
        }
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des statistiques: {e}")
        stats = {"error": str(e)}
    finally:
        db.close()
    
    return stats

def get_database_size() -> float:
    """
    Calcule la taille de la base de données en MB
    
    Returns:
        float: Taille en MB
    """
    try:
        if DATABASE_URL.startswith("sqlite"):
            db_path = DATABASE_URL.replace("sqlite:///", "")
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                return round(size_bytes / (1024 * 1024), 2)
        return 0.0
    except Exception:
        return 0.0

# Fonction utilitaire pour les migrations (si nécessaire)
def migrate_database():
    """
    Effectue les migrations de base de données si nécessaire
    
    Pour l'instant, cette fonction ne fait rien car nous utilisons
    SQLite en développement. Dans un environnement de production
    avec PostgreSQL, on pourrait utiliser Alembic ici.
    """
    print("ℹ️ Aucune migration nécessaire pour SQLite")
    pass

if __name__ == "__main__":
    # Test de la configuration de la base de données
    print("🔧 Test de la configuration de la base de données...")
    print(f"URL: {DATABASE_URL}")
    print(f"Engine: {engine.name}")
    
    if check_database_connection():
        print("✅ Connexion à la base de données OK")
        
        # Initialiser la base de données
        init_database()
        
        # Afficher les informations
        info = get_database_info()
        print(f"📊 Informations: {info}")
        
        # Afficher les statistiques
        stats = get_table_stats()
        print(f"📈 Statistiques: {stats}")
    else:
        print("❌ Impossible de se connecter à la base de données")
