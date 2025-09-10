/**
 * Composant AttackList - Liste des attaques récentes
 * Affiche les attaques en temps réel dans un format de liste
 */

import React, { useState, useEffect } from 'react';

/**
 * Composant pour un élément d'attaque individuel
 */
const AttackItem = ({ attack, isNew = false, onAttackClick }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Animation d'apparition pour les nouvelles attaques
    if (isNew) {
      const timer = setTimeout(() => setIsVisible(true), 100);
      return () => clearTimeout(timer);
    } else {
      setIsVisible(true);
    }
  }, [isNew]);

  // Formater la date pour l'affichage
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'À l\'instant';
    if (diffMins < 60) return `Il y a ${diffMins}min`;
    if (diffHours < 24) return `Il y a ${diffHours}h`;
    return `Il y a ${diffDays}j`;
  };

  // Obtenir le niveau de risque
  const getRiskLevel = (port) => {
    const criticalPorts = [22, 3389, 5432, 3306, 1433];
    const highRiskPorts = [21, 23, 25, 53, 80, 443, 993, 995];
    
    if (criticalPorts.includes(port)) return { level: 'CRITIQUE', class: 'badge-critical' };
    if (highRiskPorts.includes(port)) return { level: 'ÉLEVÉ', class: 'badge-high' };
    return { level: 'FAIBLE', class: 'badge-low' };
  };

  // Obtenir la couleur du port
  const getPortColor = (port) => {
    const portColors = {
      22: 'text-green-600 dark:text-green-400',    // SSH
      80: 'text-blue-600 dark:text-blue-400',      // HTTP
      443: 'text-yellow-600 dark:text-yellow-400', // HTTPS
      3389: 'text-red-600 dark:text-red-400',      // RDP
      5432: 'text-purple-600 dark:text-purple-400', // PostgreSQL
      3306: 'text-orange-600 dark:text-orange-400', // MySQL
      21: 'text-cyan-600 dark:text-cyan-400',      // FTP
      23: 'text-pink-600 dark:text-pink-400',      // Telnet
      25: 'text-indigo-600 dark:text-indigo-400',  // SMTP
      53: 'text-teal-600 dark:text-teal-400',      // DNS
    };
    return portColors[port] || 'text-gray-600 dark:text-gray-400';
  };

  const risk = getRiskLevel(attack.port);
  const portColor = getPortColor(attack.port);

  if (!isVisible) return null;

  return (
    <div
      className={`attack-card hover-lift cursor-pointer transition-all duration-200 ${
        isNew ? 'slide-in-right border-l-4 border-attack-red' : ''
      }`}
      onClick={() => onAttackClick && onAttackClick(attack)}
    >
      <div className="attack-card-body">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2">
              <span className="text-2xl">🚨</span>
              <span className="font-mono text-sm font-bold text-gray-900 dark:text-gray-100">
                {attack.ip_address}
              </span>
            </div>
            <span className={`badge ${risk.class}`}>
              {risk.level}
            </span>
          </div>
          <div className="text-right">
            <div className="text-xs text-gray-500 dark:text-gray-400">
              {formatDate(attack.timestamp)}
            </div>
            {isNew && (
              <div className="text-xs text-attack-red font-bold animate-pulse">
                NOUVEAU
              </div>
            )}
          </div>
        </div>
        
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-1">
              <span className="text-gray-600 dark:text-gray-400">Port:</span>
              <span className={`font-mono font-bold ${portColor}`}>
                {attack.port}
              </span>
            </div>
            
            <div className="flex items-center space-x-1">
              <span className="text-gray-600 dark:text-gray-400">Protocole:</span>
              <span className="font-mono text-gray-900 dark:text-gray-100">
                {attack.protocol}
              </span>
            </div>
          </div>
          
          <div className="text-right">
            <div className="text-gray-600 dark:text-gray-400">
              {attack.city && attack.country ? 
                `${attack.city}, ${attack.country}` : 
                attack.country || 'Localisation inconnue'
              }
            </div>
            {attack.isp && (
              <div className="text-xs text-gray-500 dark:text-gray-500 truncate max-w-[150px]">
                {attack.isp}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

/**
 * Composant principal AttackList
 */
const AttackList = ({ 
  attacks = [], 
  newAttacks = [], 
  onAttackClick,
  className = "",
  maxItems = 50 
}) => {
  const [displayedAttacks, setDisplayedAttacks] = useState([]);
  const [isAutoScroll, setIsAutoScroll] = useState(true);

  // Combiner les attaques existantes et nouvelles
  useEffect(() => {
    const allAttacks = [...attacks, ...newAttacks];
    const sortedAttacks = allAttacks
      .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
      .slice(0, maxItems);
    
    setDisplayedAttacks(sortedAttacks);
  }, [attacks, newAttacks, maxItems]);

  // Auto-scroll vers le haut pour les nouvelles attaques
  useEffect(() => {
    if (isAutoScroll && newAttacks.length > 0) {
      const listElement = document.getElementById('attack-list');
      if (listElement) {
        listElement.scrollTop = 0;
      }
    }
  }, [newAttacks, isAutoScroll]);

  // Statistiques des attaques
  const stats = {
    total: displayedAttacks.length,
    new: newAttacks.length,
    critical: displayedAttacks.filter(attack => 
      [22, 3389, 5432, 3306, 1433].includes(attack.port)
    ).length,
    countries: [...new Set(displayedAttacks.map(attack => attack.country))].length
  };

  return (
    <div className={`flex flex-col h-full ${className}`}>
      {/* En-tête avec statistiques */}
      <div className="attack-card-header">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
            📋 Attaques Récentes
          </h3>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setIsAutoScroll(!isAutoScroll)}
              className={`text-xs px-2 py-1 rounded ${
                isAutoScroll 
                  ? 'bg-attack-blue text-white' 
                  : 'bg-gray-200 dark:bg-dark-border text-gray-600 dark:text-gray-400'
              }`}
            >
              {isAutoScroll ? 'Auto-scroll ON' : 'Auto-scroll OFF'}
            </button>
          </div>
        </div>
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Total:</span>
            <span className="font-bold text-gray-900 dark:text-gray-100">{stats.total}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Nouvelles:</span>
            <span className="font-bold text-attack-red">{stats.new}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Critiques:</span>
            <span className="font-bold text-attack-red">{stats.critical}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Pays:</span>
            <span className="font-bold text-gray-900 dark:text-gray-100">{stats.countries}</span>
          </div>
        </div>
      </div>

      {/* Liste des attaques */}
      <div className="flex-1 overflow-y-auto custom-scrollbar" id="attack-list">
        {displayedAttacks.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-4xl mb-2">🛡️</div>
              <h3 className="text-lg font-bold text-gray-600 dark:text-gray-400 mb-1">
                Aucune attaque détectée
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-500">
                En attente de tentatives d'intrusion...
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-2 p-4">
            {displayedAttacks.map((attack, index) => (
              <AttackItem
                key={`${attack.id}-${index}`}
                attack={attack}
                isNew={newAttacks.some(newAttack => newAttack.id === attack.id)}
                onAttackClick={onAttackClick}
              />
            ))}
          </div>
        )}
      </div>

      {/* Pied de page avec informations */}
      <div className="attack-card-header border-t border-gray-200 dark:border-dark-border">
        <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
          Dernière mise à jour: {new Date().toLocaleTimeString('fr-FR')}
        </div>
      </div>
    </div>
  );
};

export default AttackList;
