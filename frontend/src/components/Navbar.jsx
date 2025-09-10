/**
 * Composant Navbar - Barre de navigation
 * Navigation simple avec logo et contrôles
 */

import React, { useState, useEffect } from 'react';

/**
 * Composant principal Navbar
 */
const Navbar = ({ 
  isConnected = false, 
  attackCount = 0, 
  onToggleDarkMode,
  isDarkMode = false 
}) => {
  const [currentTime, setCurrentTime] = useState(new Date());

  // Mise à jour de l'heure toutes les secondes
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Formater l'heure pour l'affichage
  const formatTime = (date) => {
    return date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <nav className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo et titre */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="text-2xl">🛡️</div>
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">
                  Honeypot Attack Map
                </h1>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  Visualisation en temps réel
                </p>
              </div>
            </div>
          </div>

          {/* Informations centrales */}
          <div className="flex items-center space-x-6">
            {/* Statut de connexion */}
            <div className="flex items-center space-x-2">
              <div className={`status-indicator ${isConnected ? 'status-online' : 'status-offline'}`}></div>
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {isConnected ? 'Connecté' : 'Déconnecté'}
              </span>
            </div>

            {/* Compteur d'attaques */}
            <div className="flex items-center space-x-2">
              <div className="text-2xl">🚨</div>
              <div className="text-right">
                <div className="text-lg font-bold text-attack-red">
                  {attackCount.toLocaleString()}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Attaques détectées
                </div>
              </div>
            </div>

            {/* Heure actuelle */}
            <div className="text-right">
              <div className="text-lg font-mono font-bold text-gray-900 dark:text-gray-100">
                {formatTime(currentTime)}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                {currentTime.toLocaleDateString('fr-FR')}
              </div>
            </div>
          </div>

          {/* Contrôles */}
          <div className="flex items-center space-x-4">
            {/* Bouton mode sombre */}
            <button
              onClick={onToggleDarkMode}
              className="p-2 rounded-lg bg-gray-100 dark:bg-dark-border hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
              title={isDarkMode ? 'Passer en mode clair' : 'Passer en mode sombre'}
            >
              {isDarkMode ? (
                <svg className="w-5 h-5 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5 text-gray-600 dark:text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                </svg>
              )}
            </button>

            {/* Menu de navigation */}
            <div className="flex items-center space-x-2">
              <a
                href="#"
                className="px-3 py-2 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 bg-attack-blue text-white"
              >
                Dashboard
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
