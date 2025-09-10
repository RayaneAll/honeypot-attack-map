import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix for default markers in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const AttackMap = ({ attacks }) => {
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markersRef = useRef([]);

  useEffect(() => {
    // Initialize map
    if (!mapInstanceRef.current) {
      mapInstanceRef.current = L.map(mapRef.current).setView([20, 0], 2);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(mapInstanceRef.current);
    }
  }, []);

  useEffect(() => {
    // Clear existing markers
    markersRef.current.forEach(marker => {
      mapInstanceRef.current.removeLayer(marker);
    });
    markersRef.current = [];

    // Add new attack markers
    attacks.forEach(attack => {
      if (attack.latitude && attack.longitude && attack.latitude !== 0 && attack.longitude !== 0) {
        const attackIcon = L.divIcon({
          className: 'attack-marker',
          html: `<div class="w-4 h-4 bg-red-500 rounded-full border-2 border-white shadow-lg"></div>`,
          iconSize: [16, 16],
          iconAnchor: [8, 8]
        });

        const marker = L.marker([attack.latitude, attack.longitude], {
          icon: attackIcon
        }).addTo(mapInstanceRef.current);

        // Add popup with attack details
        const popupContent = `
          <div class="text-sm">
            <div class="font-bold text-red-600">🚨 Attack Detected</div>
            <div class="mt-2">
              <div><strong>IP:</strong> ${attack.ip_address}</div>
              <div><strong>Port:</strong> ${attack.port}</div>
              <div><strong>Protocol:</strong> ${attack.protocol}</div>
              <div><strong>Location:</strong> ${attack.city}, ${attack.country}</div>
              <div><strong>Time:</strong> ${new Date(attack.timestamp).toLocaleString()}</div>
            </div>
          </div>
        `;

        marker.bindPopup(popupContent);
        markersRef.current.push(marker);
      }
    });

    // Fit map to show all markers
    if (markersRef.current.length > 0) {
      const group = new L.featureGroup(markersRef.current);
      mapInstanceRef.current.fitBounds(group.getBounds().pad(0.1));
    }
  }, [attacks]);

  return (
    <div className="relative h-full">
      <div 
        ref={mapRef} 
        className="w-full h-full"
        style={{ minHeight: '400px' }}
      />
      
      {/* Map overlay with attack count */}
      <div className="absolute top-4 left-4 bg-black bg-opacity-75 text-white p-3 rounded-lg">
        <div className="text-sm font-bold">Live Attacks</div>
        <div className="text-2xl font-bold text-red-400">{attacks.length}</div>
      </div>
    </div>
  );
};

export default AttackMap;
