"""
Honeypot Attack Map - Modèles SQLAlchemy
Modèles de données pour les attaques détectées par le honeypot
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any

Base = declarative_base()

class Attack(Base):
    """
    Modèle SQLAlchemy pour représenter une attaque détectée
    
    Chaque tentative de connexion au honeypot est enregistrée
    avec ses informations de géolocalisation et métadonnées.
    """
    
    __tablename__ = "attacks"
    
    # Clé primaire
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Informations de l'attaque
    ip_address = Column(String(45), nullable=False, index=True, comment="Adresse IP de l'attaquant (IPv4 ou IPv6)")
    port = Column(Integer, nullable=False, index=True, comment="Port ciblé par l'attaque")
    protocol = Column(String(10), nullable=False, default="TCP", comment="Protocole utilisé (TCP, UDP, etc.)")
    
    # Informations de géolocalisation
    country = Column(String(100), nullable=True, index=True, comment="Pays d'origine de l'attaque")
    city = Column(String(100), nullable=True, comment="Ville d'origine de l'attaque")
    latitude = Column(Float, nullable=True, comment="Latitude géographique")
    longitude = Column(Float, nullable=True, comment="Longitude géographique")
    region = Column(String(100), nullable=True, comment="Région/État d'origine")
    timezone = Column(String(50), nullable=True, comment="Fuseau horaire")
    isp = Column(String(200), nullable=True, comment="Fournisseur d'accès internet")
    
    # Métadonnées
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True, comment="Horodatage de l'attaque")
    user_agent = Column(Text, nullable=True, comment="User-Agent si disponible")
    additional_data = Column(Text, nullable=True, comment="Données supplémentaires au format JSON")
    
    # Index composés pour optimiser les requêtes
    __table_args__ = (
        Index('idx_ip_timestamp', 'ip_address', 'timestamp'),
        Index('idx_country_timestamp', 'country', 'timestamp'),
        Index('idx_port_timestamp', 'port', 'timestamp'),
    )
    
    def __repr__(self) -> str:
        """Représentation string de l'objet Attack"""
        return f"<Attack(id={self.id}, ip={self.ip_address}, port={self.port}, country={self.country})>"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Attack en dictionnaire
        
        Returns:
            Dict[str, Any]: Dictionnaire contenant toutes les données de l'attaque
        """
        return {
            "id": self.id,
            "ip_address": self.ip_address,
            "port": self.port,
            "protocol": self.protocol,
            "country": self.country,
            "city": self.city,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "region": self.region,
            "timezone": self.timezone,
            "isp": self.isp,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "user_agent": self.user_agent,
            "additional_data": self.additional_data
        }
    
    def to_websocket_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet Attack en dictionnaire optimisé pour WebSocket
        
        Returns:
            Dict[str, Any]: Dictionnaire allégé pour la transmission temps réel
        """
        return {
            "id": self.id,
            "ip_address": self.ip_address,
            "port": self.port,
            "protocol": self.protocol,
            "country": self.country or "Unknown",
            "city": self.city or "Unknown",
            "latitude": self.latitude or 0.0,
            "longitude": self.longitude or 0.0,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Attack':
        """
        Crée une instance Attack à partir d'un dictionnaire
        
        Args:
            data (Dict[str, Any]): Dictionnaire contenant les données de l'attaque
            
        Returns:
            Attack: Instance de la classe Attack
        """
        return cls(
            ip_address=data.get('ip_address'),
            port=data.get('port'),
            protocol=data.get('protocol', 'TCP'),
            country=data.get('country'),
            city=data.get('city'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            region=data.get('region'),
            timezone=data.get('timezone'),
            isp=data.get('isp'),
            timestamp=data.get('timestamp', datetime.utcnow()),
            user_agent=data.get('user_agent'),
            additional_data=data.get('additional_data')
        )
    
    def is_recent(self, hours: int = 24) -> bool:
        """
        Vérifie si l'attaque est récente
        
        Args:
            hours (int): Nombre d'heures pour considérer une attaque comme récente
            
        Returns:
            bool: True si l'attaque est récente
        """
        if not self.timestamp:
            return False
        
        from datetime import datetime, timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return self.timestamp >= cutoff_time
    
    def get_location_string(self) -> str:
        """
        Retourne une chaîne de caractères représentant la localisation
        
        Returns:
            str: Localisation formatée (ex: "Paris, France")
        """
        if self.city and self.country:
            return f"{self.city}, {self.country}"
        elif self.country:
            return self.country
        elif self.region:
            return self.region
        else:
            return "Unknown Location"
    
    def get_risk_level(self) -> str:
        """
        Détermine le niveau de risque de l'attaque basé sur le port
        
        Returns:
            str: Niveau de risque (LOW, MEDIUM, HIGH, CRITICAL)
        """
        # Ports critiques
        critical_ports = [22, 3389, 5432, 3306, 1433]  # SSH, RDP, PostgreSQL, MySQL, MSSQL
        
        # Ports sensibles
        high_risk_ports = [21, 23, 25, 53, 80, 443, 993, 995]  # FTP, Telnet, SMTP, DNS, HTTP, HTTPS, IMAPS, POP3S
        
        # Ports moyens
        medium_risk_ports = [110, 143, 993, 995, 587, 465]  # POP3, IMAP, IMAPS, POP3S, SMTP, SMTPS
        
        if self.port in critical_ports:
            return "CRITICAL"
        elif self.port in high_risk_ports:
            return "HIGH"
        elif self.port in medium_risk_ports:
            return "MEDIUM"
        else:
            return "LOW"

# Modèle pour les statistiques (optionnel)
class AttackStats(Base):
    """
    Modèle pour stocker des statistiques pré-calculées
    
    Ce modèle peut être utilisé pour optimiser les requêtes
    de statistiques fréquentes.
    """
    
    __tablename__ = "attack_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    stat_name = Column(String(100), nullable=False, unique=True, comment="Nom de la statistique")
    stat_value = Column(String(500), nullable=False, comment="Valeur de la statistique (JSON)")
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow, comment="Dernière mise à jour")
    
    def __repr__(self) -> str:
        return f"<AttackStats(name={self.stat_name}, value={self.stat_value})>"