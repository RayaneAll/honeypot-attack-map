/**
 * Page Dashboard - Page principale de l'application
 * Affiche la carte des attaques et la liste des attaques récentes
 */

import React, { useState, useEffect, useCallback } from 'react';
import AttackMap from '../components/AttackMap';
import AttackList from '../components/AttackList';
import Navbar from '../components/Navbar';
import { attackService, healthService, handleApiError } from '../services/api';
import webSocketService from '../services/websocket';

/**
 * Composant principal Dashboard
 */
const Dashboard = () => {
  // États principaux
  const [attacks, setAttacks] = useState([]);
  const [newAttacks, setNewAttacks] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [stats, setStats] = useState({
    total_attacks: 0,
    recent_attacks_24h: 0,
    top_countries: [],
    top_ports: []
  });

  // États pour les filtres
  const [filters, setFilters] = useState({
    country: '',
    protocol: '',
    port: '',
    hours: 24
  });

  // Charger les attaques depuis l'API
  const loadAttacks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const attackData = await attackService.getAttacks({
        limit: 1000,
        ...filters
      });

      setAttacks(attackData);
    } catch (err) {
      console.error('Erreur lors du chargement des attaques:', err);
      setError(handleApiError(err));
    } finally {
      setIsLoading(false);
    }
  }, [filters]);

  // Charger les statistiques
  const loadStats = useCallback(async () => {
    try {
      const statsData = await attackService.getStats();
      setStats(statsData);
    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err);
    }
  }, []);

  // Vérifier la santé de l'API
  const checkHealth = useCallback(async () => {
    try {
      const healthData = await healthService.checkHealth();
      setIsConnected(healthData.status === 'healthy');
    } catch (err) {
      console.error('Erreur lors de la vérification de la santé:', err);
      setIsConnected(false);
    }
  }, []);

  // Initialiser la connexion WebSocket
  const initWebSocket = useCallback(() => {
    webSocketService.connect()
      .then(() => {
        console.log('✅ WebSocket connecté');
        setIsConnected(true);
      })
      .catch((err) => {
        console.error('❌ Erreur de connexion WebSocket:', err);
        setIsConnected(false);
      });

    // Écouter les nouvelles attaques
    webSocketService.on('new_attack', (attackData) => {
      console.log('🚨 Nouvelle attaque reçue:', attackData);
      setNewAttacks(prev => [attackData, ...prev.slice(0, 49)]); // Garder les 50 dernières
    });

    // Écouter les changements de statut de connexion
    webSocketService.on('connected', () => {
      setIsConnected(true);
    });

    webSocketService.on('disconnected', () => {
      setIsConnected(false);
    });

    webSocketService.on('error', (err) => {
      console.error('❌ Erreur WebSocket:', err);
      setIsConnected(false);
    });
  }, []);

  // Charger le mode sombre depuis le localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setIsDarkMode(savedDarkMode);
    
    if (savedDarkMode) {
      document.documentElement.classList.add('dark');
    }
  }, []);

  // Initialisation au montage du composant
  useEffect(() => {
    loadAttacks();
    loadStats();
    checkHealth();
    initWebSocket();

    // Vérifier la santé toutes les 30 secondes
    const healthInterval = setInterval(checkHealth, 30000);

    // Nettoyage
    return () => {
      clearInterval(healthInterval);
      webSocketService.disconnect();
    };
  }, [loadAttacks, loadStats, checkHealth, initWebSocket]);

  // Recharger les attaques quand les filtres changent
  useEffect(() => {
    loadAttacks();
  }, [loadAttacks]);

  // Basculer le mode sombre
  const toggleDarkMode = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode.toString());
    
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  // Gérer le clic sur une attaque
  const handleAttackClick = (attack) => {
    console.log('Attaque cliquée:', attack);
    // Ici on pourrait ouvrir un modal avec plus de détails
  };

  // Appliquer un filtre
  const applyFilter = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  // Réinitialiser les filtres
  const resetFilters = () => {
    setFilters({
      country: '',
      protocol: '',
      port: '',
      hours: 24
    });
  };

  // Calculer le nombre total d'attaques affichées
  const totalAttacks = attacks.length + newAttacks.length;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-bg">
      {/* Navigation */}
      <Navbar
        isConnected={isConnected}
        attackCount={totalAttacks}
        onToggleDarkMode={toggleDarkMode}
        isDarkMode={isDarkMode}
      />

      {/* Contenu principal */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Filtres */}
        <div className="mb-6">
          <div className="attack-card">
            <div className="attack-card-header">
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">
                🔍 Filtres
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Pays
                  </label>
                  <select
                    value={filters.country}
                    onChange={(e) => applyFilter('country', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-border rounded-lg bg-white dark:bg-dark-card text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-attack-blue focus:border-transparent"
                  >
                    <option value="">Tous les pays</option>
                    {stats.top_countries.map(country => (
                      <option key={country.country} value={country.country}>
                        {country.country} ({country.count})
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Protocole
                  </label>
                  <select
                    value={filters.protocol}
                    onChange={(e) => applyFilter('protocol', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-border rounded-lg bg-white dark:bg-dark-card text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-attack-blue focus:border-transparent"
                  >
                    <option value="">Tous les protocoles</option>
                    <option value="TCP">TCP</option>
                    <option value="UDP">UDP</option>
                    <option value="HTTP">HTTP</option>
                    <option value="HTTPS">HTTPS</option>
                    <option value="SSH">SSH</option>
                    <option value="FTP">FTP</option>
                    <option value="SMTP">SMTP</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Port
                  </label>
                  <input
                    type="number"
                    value={filters.port}
                    onChange={(e) => applyFilter('port', e.target.value)}
                    placeholder="Ex: 22, 80, 443"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-border rounded-lg bg-white dark:bg-dark-card text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-attack-blue focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Période
                  </label>
                  <select
                    value={filters.hours}
                    onChange={(e) => applyFilter('hours', parseInt(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-dark-border rounded-lg bg-white dark:bg-dark-card text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-attack-blue focus:border-transparent"
                  >
                    <option value={1}>Dernière heure</option>
                    <option value={24}>Dernières 24h</option>
                    <option value={168}>Dernière semaine</option>
                    <option value={720}>Dernier mois</option>
                    <option value={0}>Tout</option>
                  </select>
                </div>
              </div>

              <div className="mt-4 flex justify-end">
                <button
                  onClick={resetFilters}
                  className="btn-secondary"
                >
                  Réinitialiser les filtres
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Contenu principal */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Carte des attaques */}
          <div className="lg:col-span-2">
            <div className="attack-card h-[600px]">
              <div className="attack-card-header">
                <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  🗺️ Carte des Attaques
                </h3>
              </div>
              <div className="attack-card-body p-0 h-[calc(100%-60px)]">
                {isLoading ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-attack-blue mx-auto mb-4"></div>
                      <p className="text-gray-600 dark:text-gray-400">Chargement des attaques...</p>
                    </div>
                  </div>
                ) : error ? (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="text-4xl mb-4">❌</div>
                      <h3 className="text-lg font-bold text-red-600 mb-2">Erreur de chargement</h3>
                      <p className="text-gray-600 dark:text-gray-400">{error}</p>
                    </div>
                  </div>
                ) : (
                  <AttackMap
                    attacks={attacks}
                    newAttacks={newAttacks}
                    className="h-full"
                  />
                )}
              </div>
            </div>
          </div>

          {/* Liste des attaques récentes */}
          <div className="lg:col-span-1">
            <div className="attack-card h-[600px]">
              <AttackList
                attacks={attacks}
                newAttacks={newAttacks}
                onAttackClick={handleAttackClick}
                className="h-full"
                maxItems={50}
              />
            </div>
          </div>
        </div>

        {/* Statistiques détaillées */}
        <div className="mt-6">
          <div className="attack-card">
            <div className="attack-card-header">
              <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
                📊 Statistiques Détaillées
              </h3>
            </div>
            <div className="attack-card-body">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="text-md font-bold text-gray-900 dark:text-gray-100 mb-3">
                    Top Pays
                  </h4>
                  <div className="space-y-2">
                    {stats.top_countries.slice(0, 5).map((country, index) => (
                      <div key={country.country} className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          {index + 1}. {country.country}
                        </span>
                        <span className="text-sm font-bold text-gray-900 dark:text-gray-100">
                          {country.count}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-md font-bold text-gray-900 dark:text-gray-100 mb-3">
                    Top Ports
                  </h4>
                  <div className="space-y-2">
                    {stats.top_ports.slice(0, 5).map((port, index) => (
                      <div key={port.port} className="flex justify-between items-center">
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          {index + 1}. Port {port.port}
                        </span>
                        <span className="text-sm font-bold text-gray-900 dark:text-gray-100">
                          {port.count}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-md font-bold text-gray-900 dark:text-gray-100 mb-3">
                    Résumé
                  </h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600 dark:text-gray-400">Total:</span>
                      <span className="text-sm font-bold text-gray-900 dark:text-gray-100">
                        {stats.total_attacks.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600 dark:text-gray-400">24h:</span>
                      <span className="text-sm font-bold text-attack-red">
                        {stats.recent_attacks_24h.toLocaleString()}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-gray-600 dark:text-gray-400">Pays uniques:</span>
                      <span className="text-sm font-bold text-gray-900 dark:text-gray-100">
                        {stats.top_countries.length}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
