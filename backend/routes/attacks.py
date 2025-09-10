"""
Honeypot Attack Map - Routes REST API
Endpoints pour accéder aux données des attaques
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_, or_
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from database import get_db
from models import Attack

logger = logging.getLogger(__name__)

# Création du router pour les attaques
router = APIRouter(prefix="/attacks", tags=["attacks"])

@router.get("/", response_model=List[Dict[str, Any]])
async def get_attacks(
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximum d'attaques à retourner"),
    offset: int = Query(0, ge=0, description="Décalage pour la pagination"),
    country: Optional[str] = Query(None, description="Filtrer par pays"),
    protocol: Optional[str] = Query(None, description="Filtrer par protocole"),
    port: Optional[int] = Query(None, ge=1, le=65535, description="Filtrer par port"),
    hours: Optional[int] = Query(None, ge=1, le=168, description="Filtrer les attaques des dernières X heures"),
    db: Session = Depends(get_db)
):
    """
    Récupère la liste des attaques avec filtres optionnels
    
    Args:
        limit: Nombre maximum d'attaques à retourner (1-1000)
        offset: Décalage pour la pagination
        country: Filtrer par pays
        protocol: Filtrer par protocole
        port: Filtrer par port
        hours: Filtrer les attaques des dernières X heures
        db: Session de base de données
    
    Returns:
        List[Dict]: Liste des attaques correspondant aux critères
    """
    try:
        # Construction de la requête de base
        query = db.query(Attack)
        
        # Application des filtres
        if country:
            query = query.filter(Attack.country.ilike(f"%{country}%"))
        
        if protocol:
            query = query.filter(Attack.protocol == protocol)
        
        if port:
            query = query.filter(Attack.port == port)
        
        if hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = query.filter(Attack.timestamp >= cutoff_time)
        
        # Tri par timestamp décroissant (plus récent en premier)
        query = query.order_by(desc(Attack.timestamp))
        
        # Pagination
        attacks = query.offset(offset).limit(limit).all()
        
        # Conversion en dictionnaires
        result = [attack.to_dict() for attack in attacks]
        
        logger.info(f"Récupération de {len(result)} attaques (limit={limit}, offset={offset})")
        return result
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des attaques: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/{attack_id}", response_model=Dict[str, Any])
async def get_attack(
    attack_id: int = Path(..., description="ID de l'attaque à récupérer"),
    db: Session = Depends(get_db)
):
    """
    Récupère les détails d'une attaque spécifique
    
    Args:
        attack_id: ID unique de l'attaque
        db: Session de base de données
    
    Returns:
        Dict: Détails complets de l'attaque
    """
    try:
        attack = db.query(Attack).filter(Attack.id == attack_id).first()
        
        if not attack:
            raise HTTPException(status_code=404, detail="Attaque non trouvée")
        
        logger.info(f"Récupération de l'attaque {attack_id}")
        return attack.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'attaque {attack_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/stats/summary", response_model=Dict[str, Any])
async def get_attack_summary(db: Session = Depends(get_db)):
    """
    Récupère un résumé des statistiques d'attaques
    
    Returns:
        Dict: Statistiques générales des attaques
    """
    try:
        # Total des attaques
        total_attacks = db.query(Attack).count()
        
        # Attaques des dernières 24h
        yesterday = datetime.utcnow() - timedelta(days=1)
        recent_attacks = db.query(Attack).filter(Attack.timestamp >= yesterday).count()
        
        # Attaques des dernières heures
        last_hour = datetime.utcnow() - timedelta(hours=1)
        last_hour_attacks = db.query(Attack).filter(Attack.timestamp >= last_hour).count()
        
        # Pays uniques
        unique_countries = db.query(Attack.country).distinct().count()
        
        # IPs uniques
        unique_ips = db.query(Attack.ip_address).distinct().count()
        
        # Ports les plus attaqués
        top_ports = db.query(
            Attack.port,
            func.count(Attack.id).label('count')
        ).group_by(Attack.port).order_by(func.count(Attack.id).desc()).limit(5).all()
        
        # Pays les plus actifs
        top_countries = db.query(
            Attack.country,
            func.count(Attack.id).label('count')
        ).group_by(Attack.country).order_by(func.count(Attack.id).desc()).limit(5).all()
        
        # Protocoles les plus utilisés
        top_protocols = db.query(
            Attack.protocol,
            func.count(Attack.id).label('count')
        ).group_by(Attack.protocol).order_by(func.count(Attack.id).desc()).all()
        
        summary = {
            "total_attacks": total_attacks,
            "recent_attacks_24h": recent_attacks,
            "last_hour_attacks": last_hour_attacks,
            "unique_countries": unique_countries,
            "unique_ips": unique_ips,
            "top_ports": [{"port": port, "count": count} for port, count in top_ports],
            "top_countries": [{"country": country, "count": count} for country, count in top_countries],
            "top_protocols": [{"protocol": protocol, "count": count} for protocol, count in top_protocols],
            "last_updated": datetime.utcnow().isoformat()
        }
        
        logger.info("Statistiques d'attaques récupérées")
        return summary
        
    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/stats/by-country", response_model=List[Dict[str, Any]])
async def get_attacks_by_country(
    limit: int = Query(10, ge=1, le=50, description="Nombre maximum de pays à retourner"),
    hours: Optional[int] = Query(None, ge=1, le=168, description="Filtrer les attaques des dernières X heures"),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques d'attaques par pays
    
    Args:
        limit: Nombre maximum de pays à retourner
        hours: Filtrer les attaques des dernières X heures
        db: Session de base de données
    
    Returns:
        List[Dict]: Statistiques par pays
    """
    try:
        query = db.query(
            Attack.country,
            func.count(Attack.id).label('attack_count'),
            func.count(func.distinct(Attack.ip_address)).label('unique_ips')
        ).group_by(Attack.country)
        
        if hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = query.filter(Attack.timestamp >= cutoff_time)
        
        results = query.order_by(func.count(Attack.id).desc()).limit(limit).all()
        
        stats = []
        for country, attack_count, unique_ips in results:
            stats.append({
                "country": country or "Unknown",
                "attack_count": attack_count,
                "unique_ips": unique_ips
            })
        
        logger.info(f"Statistiques par pays récupérées: {len(stats)} pays")
        return stats
        
    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques par pays: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/stats/by-port", response_model=List[Dict[str, Any]])
async def get_attacks_by_port(
    limit: int = Query(10, ge=1, le=50, description="Nombre maximum de ports à retourner"),
    hours: Optional[int] = Query(None, ge=1, le=168, description="Filtrer les attaques des dernières X heures"),
    db: Session = Depends(get_db)
):
    """
    Récupère les statistiques d'attaques par port
    
    Args:
        limit: Nombre maximum de ports à retourner
        hours: Filtrer les attaques des dernières X heures
        db: Session de base de données
    
    Returns:
        List[Dict]: Statistiques par port
    """
    try:
        query = db.query(
            Attack.port,
            func.count(Attack.id).label('attack_count'),
            func.count(func.distinct(Attack.ip_address)).label('unique_ips')
        ).group_by(Attack.port)
        
        if hours:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = query.filter(Attack.timestamp >= cutoff_time)
        
        results = query.order_by(func.count(Attack.id).desc()).limit(limit).all()
        
        stats = []
        for port, attack_count, unique_ips in results:
            stats.append({
                "port": port,
                "attack_count": attack_count,
                "unique_ips": unique_ips
            })
        
        logger.info(f"Statistiques par port récupérées: {len(stats)} ports")
        return stats
        
    except Exception as e:
        logger.error(f"Erreur lors du calcul des statistiques par port: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.get("/recent/live", response_model=List[Dict[str, Any]])
async def get_recent_live_attacks(
    minutes: int = Query(5, ge=1, le=60, description="Dernières X minutes"),
    limit: int = Query(50, ge=1, le=200, description="Nombre maximum d'attaques"),
    db: Session = Depends(get_db)
):
    """
    Récupère les attaques très récentes (pour le temps réel)
    
    Args:
        minutes: Dernières X minutes
        limit: Nombre maximum d'attaques
        db: Session de base de données
    
    Returns:
        List[Dict]: Attaques récentes
    """
    try:
        cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
        
        attacks = db.query(Attack).filter(
            Attack.timestamp >= cutoff_time
        ).order_by(desc(Attack.timestamp)).limit(limit).all()
        
        result = [attack.to_websocket_dict() for attack in attacks]
        
        logger.info(f"Récupération de {len(result)} attaques récentes (dernières {minutes} minutes)")
        return result
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des attaques récentes: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.delete("/{attack_id}")
async def delete_attack(
    attack_id: int = Path(..., description="ID de l'attaque à supprimer"),
    db: Session = Depends(get_db)
):
    """
    Supprime une attaque spécifique
    
    Args:
        attack_id: ID de l'attaque à supprimer
        db: Session de base de données
    
    Returns:
        Dict: Confirmation de suppression
    """
    try:
        attack = db.query(Attack).filter(Attack.id == attack_id).first()
        
        if not attack:
            raise HTTPException(status_code=404, detail="Attaque non trouvée")
        
        db.delete(attack)
        db.commit()
        
        logger.info(f"Attaque {attack_id} supprimée")
        return {"message": f"Attaque {attack_id} supprimée avec succès"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la suppression de l'attaque {attack_id}: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.delete("/cleanup/old")
async def cleanup_old_attacks(
    days: int = Query(30, ge=1, le=365, description="Supprimer les attaques plus anciennes que X jours"),
    db: Session = Depends(get_db)
):
    """
    Nettoie les anciennes attaques
    
    Args:
        days: Supprimer les attaques plus anciennes que X jours
        db: Session de base de données
    
    Returns:
        Dict: Résultat du nettoyage
    """
    try:
        cutoff_time = datetime.utcnow() - timedelta(days=days)
        
        # Compter les attaques à supprimer
        count_query = db.query(Attack).filter(Attack.timestamp < cutoff_time)
        count = count_query.count()
        
        if count == 0:
            return {"message": "Aucune attaque ancienne à supprimer", "deleted_count": 0}
        
        # Supprimer les attaques
        count_query.delete(synchronize_session=False)
        db.commit()
        
        logger.info(f"Nettoyage terminé: {count} attaques supprimées (plus anciennes que {days} jours)")
        return {
            "message": f"Nettoyage terminé: {count} attaques supprimées",
            "deleted_count": count,
            "cutoff_date": cutoff_time.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du nettoyage des anciennes attaques: {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")
