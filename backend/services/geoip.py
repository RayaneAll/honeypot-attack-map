"""
Honeypot Attack Map - Service de Géolocalisation IP
Service pour obtenir la localisation géographique des adresses IP
"""

import aiohttp
import asyncio
import logging
from typing import Dict, Any, Optional
import time
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class GeoIPService:
    """
    Service de géolocalisation IP utilisant des APIs gratuites
    
    Ce service utilise ip-api.com qui offre 1000 requêtes gratuites par minute
    et ne nécessite pas de clé API.
    """
    
    def __init__(self):
        """Initialise le service de géolocalisation"""
        self.base_url = "http://ip-api.com/json"
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(hours=24)  # Cache pendant 24h
        self.rate_limit_delay = 0.1  # 100ms entre les requêtes (600 req/min max)
        self.last_request_time = 0
        
        logger.info("🌍 Service de géolocalisation initialisé")
    
    async def get_location(self, ip_address: str) -> Dict[str, Any]:
        """
        Obtient la localisation d'une adresse IP
        
        Args:
            ip_address (str): Adresse IP à géolocaliser
            
        Returns:
            Dict[str, Any]: Informations de localisation
        """
        try:
            # Vérifier si l'IP est privée
            if self._is_private_ip(ip_address):
                return self._get_private_ip_location()
            
            # Vérifier le cache
            if ip_address in self.cache:
                cached_data = self.cache[ip_address]
                if self._is_cache_valid(cached_data):
                    logger.debug(f"📍 Localisation trouvée dans le cache pour {ip_address}")
                    return cached_data['location']
            
            # Respecter le rate limiting
            await self._rate_limit()
            
            # Faire la requête à l'API
            location = await self._fetch_location_from_api(ip_address)
            
            # Mettre en cache
            self.cache[ip_address] = {
                'location': location,
                'cached_at': datetime.now()
            }
            
            logger.info(f"🌍 Localisation récupérée pour {ip_address}: {location.get('country', 'Unknown')}")
            return location
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la géolocalisation de {ip_address}: {e}")
            return self._get_fallback_location()
    
    async def _fetch_location_from_api(self, ip_address: str) -> Dict[str, Any]:
        """
        Fait une requête à l'API de géolocalisation
        
        Args:
            ip_address (str): Adresse IP à géolocaliser
            
        Returns:
            Dict[str, Any]: Données de localisation
        """
        url = f"{self.base_url}/{ip_address}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if data.get('status') == 'success':
                        return {
                            'country': data.get('country', 'Unknown'),
                            'city': data.get('city', 'Unknown'),
                            'latitude': float(data.get('lat', 0.0)),
                            'longitude': float(data.get('lon', 0.0)),
                            'region': data.get('regionName', 'Unknown'),
                            'timezone': data.get('timezone', 'UTC'),
                            'isp': data.get('isp', 'Unknown'),
                            'org': data.get('org', 'Unknown'),
                            'as': data.get('as', 'Unknown')
                        }
                    else:
                        logger.warning(f"API retourne status 'fail' pour {ip_address}: {data.get('message', 'Unknown error')}")
                        return self._get_fallback_location()
                else:
                    logger.warning(f"API retourne status {response.status} pour {ip_address}")
                    return self._get_fallback_location()
    
    async def _rate_limit(self):
        """Applique le rate limiting pour respecter les limites de l'API"""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last_request
            await asyncio.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _is_private_ip(self, ip_address: str) -> bool:
        """
        Vérifie si une adresse IP est privée
        
        Args:
            ip_address (str): Adresse IP à vérifier
            
        Returns:
            bool: True si l'IP est privée
        """
        try:
            parts = ip_address.split('.')
            if len(parts) != 4:
                return True
            
            first_octet = int(parts[0])
            
            # Plages d'IP privées
            if first_octet == 10:
                return True
            elif first_octet == 172 and 16 <= int(parts[1]) <= 31:
                return True
            elif first_octet == 192 and int(parts[1]) == 168:
                return True
            elif first_octet == 127:  # localhost
                return True
            
            return False
        except (ValueError, IndexError):
            return True
    
    def _get_private_ip_location(self) -> Dict[str, Any]:
        """
        Retourne une localisation pour les IPs privées
        
        Returns:
            Dict[str, Any]: Localisation par défaut pour IPs privées
        """
        return {
            'country': 'Private Network',
            'city': 'Local Network',
            'latitude': 0.0,
            'longitude': 0.0,
            'region': 'Private',
            'timezone': 'UTC',
            'isp': 'Private Network',
            'org': 'Private Network',
            'as': 'Private'
        }
    
    def _get_fallback_location(self) -> Dict[str, Any]:
        """
        Retourne une localisation de fallback en cas d'erreur
        
        Returns:
            Dict[str, Any]: Localisation par défaut
        """
        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'latitude': 0.0,
            'longitude': 0.0,
            'region': 'Unknown',
            'timezone': 'UTC',
            'isp': 'Unknown',
            'org': 'Unknown',
            'as': 'Unknown'
        }
    
    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """
        Vérifie si les données en cache sont encore valides
        
        Args:
            cached_data (Dict[str, Any]): Données en cache
            
        Returns:
            bool: True si le cache est valide
        """
        if 'cached_at' not in cached_data:
            return False
        
        cached_at = cached_data['cached_at']
        if isinstance(cached_at, str):
            cached_at = datetime.fromisoformat(cached_at)
        
        return datetime.now() - cached_at < self.cache_duration
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Retourne des statistiques sur le cache
        
        Returns:
            Dict[str, Any]: Statistiques du cache
        """
        total_entries = len(self.cache)
        valid_entries = sum(1 for data in self.cache.values() if self._is_cache_valid(data))
        
        return {
            'total_entries': total_entries,
            'valid_entries': valid_entries,
            'expired_entries': total_entries - valid_entries,
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600
        }
    
    def clear_cache(self):
        """Vide le cache de géolocalisation"""
        self.cache.clear()
        logger.info("🧹 Cache de géolocalisation vidé")
    
    def clear_expired_cache(self):
        """Supprime les entrées expirées du cache"""
        expired_keys = [
            key for key, data in self.cache.items()
            if not self._is_cache_valid(data)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        logger.info(f"🧹 {len(expired_keys)} entrées expirées supprimées du cache")

# Instance globale du service
geoip_service = GeoIPService()

# Fonction utilitaire pour tester le service
async def test_geoip_service():
    """Test du service de géolocalisation"""
    test_ips = [
        "8.8.8.8",      # Google DNS
        "1.1.1.1",      # Cloudflare DNS
        "192.168.1.1",  # IP privée
        "127.0.0.1"     # localhost
    ]
    
    print("🧪 Test du service de géolocalisation...")
    
    for ip in test_ips:
        try:
            location = await geoip_service.get_location(ip)
            print(f"📍 {ip}: {location['country']}, {location['city']}")
        except Exception as e:
            print(f"❌ Erreur pour {ip}: {e}")
    
    # Afficher les statistiques du cache
    stats = geoip_service.get_cache_stats()
    print(f"📊 Statistiques du cache: {stats}")

if __name__ == "__main__":
    # Test du service
    asyncio.run(test_geoip_service())
