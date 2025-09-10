import React from 'react';

const StatsPanel = ({ stats }) => {
  const formatNumber = (num) => {
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
    return num.toString();
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-bold text-white">Attack Statistics</h3>
      
      {/* Main Stats */}
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-gray-700 rounded-lg p-3">
          <div className="text-2xl font-bold text-red-400">
            {formatNumber(stats.total_attacks || 0)}
          </div>
          <div className="text-sm text-gray-400">Total Attacks</div>
        </div>
        
        <div className="bg-gray-700 rounded-lg p-3">
          <div className="text-2xl font-bold text-yellow-400">
            {formatNumber(stats.recent_attacks_24h || 0)}
          </div>
          <div className="text-sm text-gray-400">Last 24h</div>
        </div>
      </div>
      
      {/* Top Countries */}
      {stats.top_countries && stats.top_countries.length > 0 && (
        <div>
          <h4 className="text-sm font-bold text-gray-300 mb-2">Top Countries</h4>
          <div className="space-y-1">
            {stats.top_countries.slice(0, 5).map((country, index) => (
              <div key={country.country} className="flex items-center justify-between text-sm">
                <div className="flex items-center space-x-2">
                  <span className="text-gray-400">#{index + 1}</span>
                  <span className="text-white">{country.country}</span>
                </div>
                <span className="text-red-400 font-bold">{country.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Protocol Stats */}
      {stats.protocol_stats && stats.protocol_stats.length > 0 && (
        <div>
          <h4 className="text-sm font-bold text-gray-300 mb-2">Protocols</h4>
          <div className="space-y-1">
            {stats.protocol_stats.map((protocol, index) => (
              <div key={protocol.protocol} className="flex items-center justify-between text-sm">
                <span className="text-white">{protocol.protocol}</span>
                <span className="text-blue-400 font-bold">{protocol.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default StatsPanel;
