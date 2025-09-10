/**
 * Service API pour communiquer avec le backend
 * Gère toutes les requêtes REST vers l'API du honeypot
 */

import axios from 'axios';

// Configuration de base d'axios
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Intercepteur pour les requêtes
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Intercepteur pour les réponses
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.status, error.message);
    return Promise.reject(error);
  }
);

/**
 * Service pour les attaques
 */
export const attackService = {
  /**
   * Récupère la liste des attaques avec filtres optionnels
   * @param {Object} params - Paramètres de filtrage
   * @param {number} params.limit - Nombre maximum d'attaques
   * @param {number} params.offset - Décalage pour la pagination
   * @param {string} params.country - Filtrer par pays
   * @param {string} params.protocol - Filtrer par protocole
   * @param {number} params.port - Filtrer par port
   * @param {number} params.hours - Filtrer les attaques des dernières X heures
   * @returns {Promise<Array>} Liste des attaques
   */
  async getAttacks(params = {}) {
    try {
      const response = await api.get('/api/attacks/', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des attaques:', error);
      throw error;
    }
  },

  /**
   * Récupère une attaque spécifique par ID
   * @param {number} id - ID de l'attaque
   * @returns {Promise<Object>} Détails de l'attaque
   */
  async getAttackById(id) {
    try {
      const response = await api.get(`/api/attacks/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la récupération de l'attaque ${id}:`, error);
      throw error;
    }
  },

  /**
   * Récupère les statistiques des attaques
   * @returns {Promise<Object>} Statistiques des attaques
   */
  async getStats() {
    try {
      const response = await api.get('/api/attacks/stats/summary');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques:', error);
      throw error;
    }
  },

  /**
   * Récupère les statistiques par pays
   * @param {Object} params - Paramètres de filtrage
   * @returns {Promise<Array>} Statistiques par pays
   */
  async getStatsByCountry(params = {}) {
    try {
      const response = await api.get('/api/attacks/stats/by-country', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques par pays:', error);
      throw error;
    }
  },

  /**
   * Récupère les statistiques par port
   * @param {Object} params - Paramètres de filtrage
   * @returns {Promise<Array>} Statistiques par port
   */
  async getStatsByPort(params = {}) {
    try {
      const response = await api.get('/api/attacks/stats/by-port', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques par port:', error);
      throw error;
    }
  },

  /**
   * Récupère les attaques récentes pour le temps réel
   * @param {Object} params - Paramètres de filtrage
   * @returns {Promise<Array>} Attaques récentes
   */
  async getRecentAttacks(params = {}) {
    try {
      const response = await api.get('/api/attacks/recent/live', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des attaques récentes:', error);
      throw error;
    }
  },

  /**
   * Supprime une attaque
   * @param {number} id - ID de l'attaque à supprimer
   * @returns {Promise<Object>} Confirmation de suppression
   */
  async deleteAttack(id) {
    try {
      const response = await api.delete(`/api/attacks/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Erreur lors de la suppression de l'attaque ${id}:`, error);
      throw error;
    }
  },

  /**
   * Nettoie les anciennes attaques
   * @param {Object} params - Paramètres de nettoyage
   * @returns {Promise<Object>} Résultat du nettoyage
   */
  async cleanupOldAttacks(params = {}) {
    try {
      const response = await api.delete('/api/attacks/cleanup/old', { params });
      return response.data;
    } catch (error) {
      console.error('Erreur lors du nettoyage des anciennes attaques:', error);
      throw error;
    }
  }
};

/**
 * Service pour la santé de l'API
 */
export const healthService = {
  /**
   * Vérifie l'état de santé de l'API
   * @returns {Promise<Object>} État de santé
   */
  async checkHealth() {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la vérification de la santé:', error);
      throw error;
    }
  },

  /**
   * Récupère les informations générales de l'API
   * @returns {Promise<Object>} Informations de l'API
   */
  async getInfo() {
    try {
      const response = await api.get('/');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des informations:', error);
      throw error;
    }
  }
};

/**
 * Service pour les statistiques générales
 */
export const statsService = {
  /**
   * Récupère les statistiques générales
   * @returns {Promise<Object>} Statistiques générales
   */
  async getGeneralStats() {
    try {
      const response = await api.get('/stats');
      return response.data;
    } catch (error) {
      console.error('Erreur lors de la récupération des statistiques générales:', error);
      throw error;
    }
  }
};

/**
 * Fonction utilitaire pour gérer les erreurs API
 * @param {Error} error - Erreur à traiter
 * @returns {string} Message d'erreur formaté
 */
export const handleApiError = (error) => {
  if (error.response) {
    // Erreur de réponse du serveur
    const status = error.response.status;
    const message = error.response.data?.detail || error.response.data?.message || 'Erreur du serveur';
    
    switch (status) {
      case 400:
        return `Erreur de requête: ${message}`;
      case 401:
        return 'Non autorisé. Veuillez vous connecter.';
      case 403:
        return 'Accès interdit.';
      case 404:
        return 'Ressource non trouvée.';
      case 500:
        return 'Erreur interne du serveur.';
      default:
        return `Erreur ${status}: ${message}`;
    }
  } else if (error.request) {
    // Erreur de réseau
    return 'Erreur de connexion. Vérifiez votre connexion internet.';
  } else {
    // Autre erreur
    return `Erreur: ${error.message}`;
  }
};

/**
 * Fonction utilitaire pour formater les données d'attaque
 * @param {Object} attack - Données d'attaque brutes
 * @returns {Object} Données d'attaque formatées
 */
export const formatAttackData = (attack) => {
  return {
    id: attack.id,
    ip_address: attack.ip_address,
    port: attack.port,
    protocol: attack.protocol || 'TCP',
    country: attack.country || 'Unknown',
    city: attack.city || 'Unknown',
    latitude: attack.latitude || 0,
    longitude: attack.longitude || 0,
    region: attack.region || 'Unknown',
    timezone: attack.timezone || 'UTC',
    isp: attack.isp || 'Unknown',
    timestamp: attack.timestamp ? new Date(attack.timestamp) : new Date(),
    user_agent: attack.user_agent,
    additional_data: attack.additional_data
  };
};

export default api;
