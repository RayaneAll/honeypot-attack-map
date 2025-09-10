/**
 * Service WebSocket pour la communication temps réel
 * Gère la connexion WebSocket avec le backend pour recevoir les nouvelles attaques
 */

import { io } from 'socket.io-client';

class WebSocketService {
  constructor() {
    this.socket = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 5000; // 5 secondes
    this.listeners = new Map();
    
    // Configuration WebSocket
    this.wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
  }

  /**
   * Initialise la connexion WebSocket
   * @param {Object} options - Options de connexion
   * @returns {Promise<void>}
   */
  async connect(options = {}) {
    try {
      console.log('🔌 Connexion au WebSocket...');
      
      this.socket = io(this.wsUrl, {
        transports: ['websocket'],
        timeout: 10000,
        ...options
      });

      this.setupEventListeners();
      
      return new Promise((resolve, reject) => {
        this.socket.on('connect', () => {
          console.log('✅ WebSocket connecté');
          this.isConnected = true;
          this.reconnectAttempts = 0;
          resolve();
        });

        this.socket.on('connect_error', (error) => {
          console.error('❌ Erreur de connexion WebSocket:', error);
          reject(error);
        });

        // Timeout de connexion
        setTimeout(() => {
          if (!this.isConnected) {
            reject(new Error('Timeout de connexion WebSocket'));
          }
        }, 10000);
      });
    } catch (error) {
      console.error('❌ Erreur lors de la connexion WebSocket:', error);
      throw error;
    }
  }

  /**
   * Configure les écouteurs d'événements WebSocket
   */
  setupEventListeners() {
    if (!this.socket) return;

    // Connexion établie
    this.socket.on('connect', () => {
      console.log('✅ WebSocket connecté');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.emit('connected');
    });

    // Déconnexion
    this.socket.on('disconnect', (reason) => {
      console.log('🔌 WebSocket déconnecté:', reason);
      this.isConnected = false;
      this.emit('disconnected', reason);
      
      // Tentative de reconnexion automatique
      if (this.reconnectAttempts < this.maxReconnectAttempts) {
        this.scheduleReconnect();
      }
    });

    // Erreur de connexion
    this.socket.on('connect_error', (error) => {
      console.error('❌ Erreur de connexion WebSocket:', error);
      this.isConnected = false;
      this.emit('error', error);
    });

    // Nouvelle attaque reçue
    this.socket.on('new_attack', (attackData) => {
      console.log('🚨 Nouvelle attaque reçue:', attackData);
      this.emit('new_attack', attackData);
    });

    // Message de confirmation
    this.socket.on('connected', (data) => {
      console.log('📡 Message de confirmation reçu:', data);
      this.emit('message', data);
    });

    // Gestion des erreurs
    this.socket.on('error', (error) => {
      console.error('❌ Erreur WebSocket:', error);
      this.emit('error', error);
    });
  }

  /**
   * Planifie une tentative de reconnexion
   */
  scheduleReconnect() {
    this.reconnectAttempts++;
    const delay = this.reconnectInterval * this.reconnectAttempts;
    
    console.log(`🔄 Tentative de reconnexion ${this.reconnectAttempts}/${this.maxReconnectAttempts} dans ${delay}ms`);
    
    setTimeout(() => {
      if (!this.isConnected && this.reconnectAttempts <= this.maxReconnectAttempts) {
        this.connect();
      }
    }, delay);
  }

  /**
   * Ajoute un écouteur d'événement
   * @param {string} event - Nom de l'événement
   * @param {Function} callback - Fonction de callback
   */
  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  /**
   * Supprime un écouteur d'événement
   * @param {string} event - Nom de l'événement
   * @param {Function} callback - Fonction de callback à supprimer
   */
  off(event, callback) {
    if (this.listeners.has(event)) {
      const callbacks = this.listeners.get(event);
      const index = callbacks.indexOf(callback);
      if (index > -1) {
        callbacks.splice(index, 1);
      }
    }
  }

  /**
   * Émet un événement personnalisé
   * @param {string} event - Nom de l'événement
   * @param {*} data - Données à transmettre
   */
  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`❌ Erreur dans le callback pour l'événement ${event}:`, error);
        }
      });
    }
  }

  /**
   * Envoie un message au serveur
   * @param {string} event - Nom de l'événement
   * @param {*} data - Données à envoyer
   */
  send(event, data) {
    if (this.socket && this.isConnected) {
      this.socket.emit(event, data);
    } else {
      console.warn('⚠️ WebSocket non connecté, impossible d\'envoyer le message');
    }
  }

  /**
   * Déconnecte le WebSocket
   */
  disconnect() {
    if (this.socket) {
      console.log('🔌 Déconnexion du WebSocket...');
      this.socket.disconnect();
      this.socket = null;
      this.isConnected = false;
      this.listeners.clear();
    }
  }

  /**
   * Vérifie si le WebSocket est connecté
   * @returns {boolean} État de la connexion
   */
  getConnectionStatus() {
    return this.isConnected;
  }

  /**
   * Obtient l'ID de la session WebSocket
   * @returns {string|null} ID de la session
   */
  getSessionId() {
    return this.socket?.id || null;
  }

  /**
   * Obtient les statistiques de connexion
   * @returns {Object} Statistiques de connexion
   */
  getStats() {
    return {
      isConnected: this.isConnected,
      reconnectAttempts: this.reconnectAttempts,
      maxReconnectAttempts: this.maxReconnectAttempts,
      sessionId: this.getSessionId(),
      listenersCount: Array.from(this.listeners.values()).reduce((total, callbacks) => total + callbacks.length, 0)
    };
  }
}

// Instance singleton du service WebSocket
const webSocketService = new WebSocketService();

export default webSocketService;

/**
 * Hook React pour utiliser le service WebSocket
 * @param {Object} options - Options de connexion
 * @returns {Object} État et méthodes du WebSocket
 */
export const useWebSocket = (options = {}) => {
  const [isConnected, setIsConnected] = React.useState(false);
  const [error, setError] = React.useState(null);
  const [lastMessage, setLastMessage] = React.useState(null);

  React.useEffect(() => {
    // Connexion au WebSocket
    webSocketService.connect(options)
      .then(() => {
        setIsConnected(true);
        setError(null);
      })
      .catch((err) => {
        setError(err);
        setIsConnected(false);
      });

    // Écouteurs d'événements
    const handleConnect = () => setIsConnected(true);
    const handleDisconnect = () => setIsConnected(false);
    const handleError = (err) => setError(err);
    const handleMessage = (data) => setLastMessage(data);

    webSocketService.on('connected', handleConnect);
    webSocketService.on('disconnected', handleDisconnect);
    webSocketService.on('error', handleError);
    webSocketService.on('new_attack', handleMessage);

    // Nettoyage
    return () => {
      webSocketService.off('connected', handleConnect);
      webSocketService.off('disconnected', handleDisconnect);
      webSocketService.off('error', handleError);
      webSocketService.off('new_attack', handleMessage);
      webSocketService.disconnect();
    };
  }, []);

  return {
    isConnected,
    error,
    lastMessage,
    send: webSocketService.send.bind(webSocketService),
    disconnect: webSocketService.disconnect.bind(webSocketService),
    getStats: webSocketService.getStats.bind(webSocketService)
  };
};
