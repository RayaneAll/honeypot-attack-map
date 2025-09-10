"""
Honeypot Attack Map - Serveur Honeypot TCP
Serveur qui écoute sur un port et capture les tentatives de connexion
"""

import socket
import threading
import logging
from typing import Callable, Optional
import time

logger = logging.getLogger(__name__)

class HoneypotServer:
    """
    Serveur honeypot TCP qui capture les tentatives de connexion
    
    Ce serveur écoute sur un port spécifique et enregistre chaque tentative
    de connexion avec l'adresse IP source et le port ciblé.
    """
    
    def __init__(self, port: int = 2222, on_attack_callback: Optional[Callable] = None):
        """
        Initialise le serveur honeypot
        
        Args:
            port (int): Port sur lequel écouter (défaut: 2222)
            on_attack_callback (Callable): Fonction appelée lors d'une attaque
        """
        self.port = port
        self.on_attack_callback = on_attack_callback
        self.socket: Optional[socket.socket] = None
        self.running = False
        self.server_thread: Optional[threading.Thread] = None
        
        logger.info(f"🔧 Honeypot initialisé pour le port {port}")
    
    def start(self):
        """
        Démarre le serveur honeypot dans un thread séparé
        
        Le serveur écoute en continu et accepte toutes les connexions
        entrantes pour les logger comme des tentatives d'attaque.
        """
        if self.running:
            logger.warning("⚠️ Le honeypot est déjà en cours d'exécution")
            return
        
        self.running = True
        self.server_thread = threading.Thread(target=self._run_server, daemon=True)
        self.server_thread.start()
        logger.info(f"🔥 Honeypot démarré sur le port {self.port}")
    
    def stop(self):
        """
        Arrête le serveur honeypot
        
        Ferme la socket et attend que le thread se termine proprement.
        """
        if not self.running:
            logger.warning("⚠️ Le honeypot n'est pas en cours d'exécution")
            return
        
        self.running = False
        
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                logger.error(f"Erreur lors de la fermeture de la socket: {e}")
        
        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=5)
        
        logger.info("✅ Honeypot arrêté")
    
    def _run_server(self):
        """
        Boucle principale du serveur honeypot
        
        Cette méthode s'exécute dans un thread séparé et gère
        les connexions entrantes de manière asynchrone.
        """
        try:
            # Créer la socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Lier à l'adresse et au port
            self.socket.bind(('0.0.0.0', self.port))
            self.socket.listen(5)
            
            logger.info(f"🎯 Honeypot en écoute sur 0.0.0.0:{self.port}")
            
            while self.running:
                try:
                    # Accepter une connexion
                    client_socket, address = self.socket.accept()
                    
                    # Traiter la connexion dans un thread séparé
                    client_thread = threading.Thread(
                        target=self._handle_connection,
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                    
                except socket.error as e:
                    if self.running:
                        logger.error(f"Erreur socket: {e}")
                    break
                except Exception as e:
                    logger.error(f"Erreur inattendue: {e}")
                    break
                    
        except Exception as e:
            logger.error(f"Erreur critique du serveur honeypot: {e}")
        finally:
            self._cleanup()
    
    def _handle_connection(self, client_socket: socket.socket, address: tuple):
        """
        Gère une connexion entrante
        
        Args:
            client_socket (socket.socket): Socket du client
            address (tuple): Adresse (IP, port) du client
        """
        ip_address, port = address
        
        try:
            logger.info(f"🔍 Connexion détectée depuis {ip_address}:{port}")
            
            # Simuler une réponse pour maintenir la connexion un moment
            # Cela permet de capturer plus d'informations sur l'attaque
            try:
                # Attendre un peu pour voir si des données sont envoyées
                client_socket.settimeout(5.0)
                data = client_socket.recv(1024)
                
                if data:
                    logger.info(f"📦 Données reçues de {ip_address}: {data[:100]}...")
                
                # Envoyer une réponse factice pour maintenir la connexion
                fake_response = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2\r\n"
                client_socket.send(fake_response)
                
            except socket.timeout:
                logger.debug(f"Timeout de connexion pour {ip_address}")
            except Exception as e:
                logger.debug(f"Erreur lors de la lecture des données: {e}")
            
            # Appeler le callback d'attaque
            if self.on_attack_callback:
                try:
                    # Exécuter le callback de manière asynchrone
                    import asyncio
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(
                        self.on_attack_callback(ip_address, self.port, "TCP")
                    )
                    loop.close()
                except Exception as e:
                    logger.error(f"Erreur dans le callback d'attaque: {e}")
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la connexion {ip_address}: {e}")
        finally:
            try:
                client_socket.close()
            except Exception as e:
                logger.debug(f"Erreur lors de la fermeture de la socket client: {e}")
    
    def _cleanup(self):
        """Nettoie les ressources du serveur"""
        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None
        
        self.running = False
        logger.info("🧹 Nettoyage du serveur honeypot terminé")
    
    def is_running(self) -> bool:
        """
        Vérifie si le serveur est en cours d'exécution
        
        Returns:
            bool: True si le serveur est actif
        """
        return self.running and self.socket is not None
    
    def get_port(self) -> int:
        """
        Retourne le port sur lequel le honeypot écoute
        
        Returns:
            int: Numéro de port
        """
        return self.port

# Fonction utilitaire pour tester le honeypot
def test_honeypot_connection(host: str = "localhost", port: int = 2222):
    """
    Teste la connexion au honeypot (utile pour les tests)
    
    Args:
        host (str): Adresse du serveur
        port (int): Port du serveur
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            logger.info(f"✅ Connexion au honeypot {host}:{port} réussie")
            return True
        else:
            logger.warning(f"❌ Impossible de se connecter au honeypot {host}:{port}")
            return False
    except Exception as e:
        logger.error(f"❌ Erreur lors du test de connexion: {e}")
        return False

if __name__ == "__main__":
    # Test du honeypot en mode standalone
    logging.basicConfig(level=logging.INFO)
    
    def dummy_callback(ip, port, protocol):
        print(f"🚨 Attaque simulée: {ip}:{port} ({protocol})")
    
    honeypot = HoneypotServer(port=2222, on_attack_callback=dummy_callback)
    
    try:
        honeypot.start()
        print("Honeypot démarré. Appuyez sur Ctrl+C pour arrêter...")
        
        # Maintenir le programme en vie
        while honeypot.is_running():
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nArrêt du honeypot...")
        honeypot.stop()
