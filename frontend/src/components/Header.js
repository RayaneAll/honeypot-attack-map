import React from 'react';

const Header = ({ isConnected }) => {
  return (
    <header className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="text-2xl">🛡️</div>
          <div>
            <h1 className="text-2xl font-bold text-white">Honeypot Attack Map</h1>
            <p className="text-sm text-gray-400">Real-time cybersecurity threat visualization</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          {/* Connection Status */}
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`}></div>
            <span className="text-sm text-gray-300">
              {isConnected ? 'Live Feed' : 'Disconnected'}
            </span>
          </div>
          
          {/* Last Updated */}
          <div className="text-sm text-gray-400">
            Last updated: {new Date().toLocaleTimeString()}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
