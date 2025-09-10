/**
 * Composant AttackMap - Carte interactive des attaques
 * Utilise Leaflet.js pour afficher les attaques sur une carte du monde
 */

import React, { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix pour les icônes Leaflet avec Vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

/**
 * Composant pour créer des marqueurs d'attaque personnalisés
 */
const AttackMarker = ({ attack, isNew = false }) => {
  const markerRef = useRef(null);
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    if (markerRef.current && isNew) {
      // Animation pour les nouvelles attaques
      const marker = markerRef.current;
      marker.openPopup();
      
      // Effet de pulsation
      const interval = setInterval(() => {
        marker.getElement()?.classList.toggle('attack-pulse');
      }, 1000);
      
      return () => clearInterval(interval);
    }
  }, [isNew]);

  // Créer une icône personnalisée basée sur le niveau de risque
  const getRiskIcon = (port) => {
    const criticalPorts = [22, 3389, 5432, 3306, 1433];
    const highRiskPorts = [21, 23, 25, 53, 80, 443, 993, 995];
    
    let color = '#22c55e'; // Vert par défaut (LOW)
    if (criticalPorts.includes(port)) {
      color = '#ef4444'; // Rouge (CRITICAL)
    } else if (highRiskPorts.includes(port)) {
      color = '#f97316'; // Orange (HIGH)
    }

    return L.divIcon({
      className: 'attack-marker',
      html: `
        <div class="w-4 h-4 rounded-full border-2 border-white shadow-lg" 
             style="background-color: ${color}; animation: ${isNew ? 'attackPulse 2s infinite' : 'none'};">
        </div>
      `,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
      popupAnchor: [0, -8]
    });
  };

  // Formater la date pour l'affichage
  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString('fr-FR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  // Obtenir le niveau de risque
  const getRiskLevel = (port) => {
    const criticalPorts = [22, 3389, 5432, 3306, 1433];
    const highRiskPorts = [21, 23, 25, 53, 80, 443, 993, 995];
    
    if (criticalPorts.includes(port)) return 'CRITIQUE';
    if (highRiskPorts.includes(port)) return 'ÉLEVÉ';
    return 'FAIBLE';
  };

  // Obtenir la classe CSS pour le niveau de risque
  const getRiskClass = (port) => {
    const criticalPorts = [22, 3389, 5432, 3306, 1433];
    const highRiskPorts = [21, 23, 25, 53, 80, 443, 993, 995];
    
    if (criticalPorts.includes(port)) return 'badge-critical';
    if (highRiskPorts.includes(port)) return 'badge-high';
    return 'badge-low';
  };

  if (!isVisible || !attack.latitude || !attack.longitude) {
    return null;
  }

  return (
    <Marker
      ref={markerRef}
      position={[attack.latitude, attack.longitude]}
      icon={getRiskIcon(attack.port)}
    >
      <Popup>
        <div className="p-2 min-w-[250px]">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100">
              🚨 Attaque Détectée
            </h3>
            <span className={`badge ${getRiskClass(attack.port)}`}>
              {getRiskLevel(attack.port)}
            </span>
          </div>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="font-medium text-gray-600 dark:text-gray-400">IP:</span>
              <span className="font-mono text-gray-900 dark:text-gray-100">{attack.ip_address}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="font-medium text-gray-600 dark:text-gray-400">Port:</span>
              <span className="font-mono text-gray-900 dark:text-gray-100">{attack.port}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="font-medium text-gray-600 dark:text-gray-400">Protocole:</span>
              <span className="font-mono text-gray-900 dark:text-gray-100">{attack.protocol}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="font-medium text-gray-600 dark:text-gray-400">Localisation:</span>
              <span className="text-gray-900 dark:text-gray-100">
                {attack.city}, {attack.country}
              </span>
            </div>
            
            <div className="flex justify-between">
              <span className="font-medium text-gray-600 dark:text-gray-400">Heure:</span>
              <span className="text-gray-900 dark:text-gray-100">
                {formatDate(attack.timestamp)}
              </span>
            </div>
            
            {attack.isp && (
              <div className="flex justify-between">
                <span className="font-medium text-gray-600 dark:text-gray-400">ISP:</span>
                <span className="text-gray-900 dark:text-gray-100 truncate max-w-[150px]">
                  {attack.isp}
                </span>
              </div>
            )}
          </div>
        </div>
      </Popup>
    </Marker>
  );
};

/**
 * Composant pour ajuster automatiquement la vue de la carte
 */
const MapController = ({ attacks }) => {
  const map = useMap();

  useEffect(() => {
    if (attacks.length > 0) {
      // Filtrer les attaques avec des coordonnées valides
      const validAttacks = attacks.filter(attack => 
        attack.latitude && attack.longitude && 
        attack.latitude !== 0 && attack.longitude !== 0
      );

      if (validAttacks.length > 0) {
        // Créer des bounds pour ajuster la vue
        const bounds = L.latLngBounds(
          validAttacks.map(attack => [attack.latitude, attack.longitude])
        );
        
        // Ajuster la vue avec un padding
        map.fitBounds(bounds, { padding: [20, 20] });
      }
    }
  }, [attacks, map]);

  return null;
};

/**
 * Composant principal AttackMap
 */
const AttackMap = ({ attacks = [], newAttacks = [], className = "" }) => {
  const [mapCenter, setMapCenter] = useState([20, 0]);
  const [mapZoom, setMapZoom] = useState(2);
  const [isMapReady, setIsMapReady] = useState(false);

  // Filtrer les attaques avec des coordonnées valides
  const validAttacks = attacks.filter(attack => 
    attack.latitude && attack.longitude && 
    attack.latitude !== 0 && attack.longitude !== 0
  );

  const validNewAttacks = newAttacks.filter(attack => 
    attack.latitude && attack.longitude && 
    attack.latitude !== 0 && attack.longitude !== 0
  );

  // Statistiques des attaques
  const attackStats = {
    total: validAttacks.length,
    new: validNewAttacks.length,
    countries: [...new Set(validAttacks.map(attack => attack.country))].length,
    critical: validAttacks.filter(attack => [22, 3389, 5432, 3306, 1433].includes(attack.port)).length
  };

  return (
    <div className={`relative ${className}`}>
      {/* Statistiques en overlay */}
      <div className="absolute top-4 left-4 z-[1000] bg-white dark:bg-dark-card rounded-lg shadow-lg p-4 min-w-[200px]">
        <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2">
          📊 Statistiques
        </h3>
        <div className="space-y-1 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Total:</span>
            <span className="font-bold text-gray-900 dark:text-gray-100">{attackStats.total}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Nouvelles:</span>
            <span className="font-bold text-attack-red">{attackStats.new}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Pays:</span>
            <span className="font-bold text-gray-900 dark:text-gray-100">{attackStats.countries}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600 dark:text-gray-400">Critiques:</span>
            <span className="font-bold text-attack-red">{attackStats.critical}</span>
          </div>
        </div>
      </div>

      {/* Légende */}
      <div className="absolute top-4 right-4 z-[1000] bg-white dark:bg-dark-card rounded-lg shadow-lg p-4 min-w-[150px]">
        <h3 className="text-lg font-bold text-gray-900 dark:text-gray-100 mb-2">
          🎯 Légende
        </h3>
        <div className="space-y-1 text-sm">
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Critique</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-orange-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Élevé</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
            <span className="text-gray-600 dark:text-gray-400">Faible</span>
          </div>
        </div>
      </div>

      {/* Carte Leaflet */}
      <div className="w-full h-full rounded-lg overflow-hidden">
        <MapContainer
          center={mapCenter}
          zoom={mapZoom}
          style={{ height: '100%', width: '100%' }}
          whenReady={() => setIsMapReady(true)}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {/* Contrôleur pour ajuster la vue */}
          <MapController attacks={validAttacks} />
          
          {/* Marqueurs des attaques existantes */}
          {isMapReady && validAttacks.map((attack, index) => (
            <AttackMarker
              key={`${attack.id}-${index}`}
              attack={attack}
              isNew={false}
            />
          ))}
          
          {/* Marqueurs des nouvelles attaques */}
          {isMapReady && validNewAttacks.map((attack, index) => (
            <AttackMarker
              key={`new-${attack.id}-${index}`}
              attack={attack}
              isNew={true}
            />
          ))}
        </MapContainer>
      </div>

      {/* Message si aucune attaque */}
      {validAttacks.length === 0 && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100 dark:bg-dark-card rounded-lg">
          <div className="text-center">
            <div className="text-6xl mb-4">🛡️</div>
            <h3 className="text-xl font-bold text-gray-600 dark:text-gray-400 mb-2">
              Aucune attaque détectée
            </h3>
            <p className="text-gray-500 dark:text-gray-500">
              En attente de tentatives d'intrusion...
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default AttackMap;
