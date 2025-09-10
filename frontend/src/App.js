import React, { useState, useEffect } from 'react';
import AttackMap from './components/AttackMap';
import AttackList from './components/AttackList';
import StatsPanel from './components/StatsPanel';
import FilterPanel from './components/FilterPanel';
import Header from './components/Header';
import { io } from 'socket.io-client';
import axios from 'axios';

function App() {
  const [attacks, setAttacks] = useState([]);
  const [stats, setStats] = useState({});
  const [filters, setFilters] = useState({
    country: '',
    protocol: '',
    timeRange: '24h'
  });
  const [isConnected, setIsConnected] = useState(false);
  const [socket, setSocket] = useState(null);

  // Initialize socket connection
  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);

    newSocket.on('connect', () => {
      console.log('Connected to honeypot feed');
      setIsConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from honeypot feed');
      setIsConnected(false);
    });

    newSocket.on('new_attack', (attack) => {
      console.log('New attack received:', attack);
      setAttacks(prev => [attack, ...prev.slice(0, 999)]); // Keep last 1000 attacks
    });

    return () => {
      newSocket.close();
    };
  }, []);

  // Load initial data
  useEffect(() => {
    loadAttacks();
    loadStats();
  }, [filters]);

  const loadAttacks = async () => {
    try {
      const params = new URLSearchParams();
      if (filters.country) params.append('country', filters.country);
      if (filters.protocol) params.append('protocol', filters.protocol);
      
      const response = await axios.get(`http://localhost:5000/api/attacks?${params}`);
      setAttacks(response.data);
    } catch (error) {
      console.error('Error loading attacks:', error);
    }
  };

  const loadStats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters({ ...filters, ...newFilters });
  };

  const clearFilters = () => {
    setFilters({ country: '', protocol: '', timeRange: '24h' });
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header isConnected={isConnected} />
      
      <div className="flex h-screen">
        {/* Left Panel - Map */}
        <div className="flex-1 relative">
          <AttackMap attacks={attacks} />
        </div>
        
        {/* Right Panel - Controls and Data */}
        <div className="w-96 bg-gray-800 border-l border-gray-700 flex flex-col">
          {/* Stats Panel */}
          <div className="p-4 border-b border-gray-700">
            <StatsPanel stats={stats} />
          </div>
          
          {/* Filter Panel */}
          <div className="p-4 border-b border-gray-700">
            <FilterPanel 
              filters={filters} 
              onFilterChange={handleFilterChange}
              onClearFilters={clearFilters}
            />
          </div>
          
          {/* Attack List */}
          <div className="flex-1 overflow-hidden">
            <AttackList attacks={attacks} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
