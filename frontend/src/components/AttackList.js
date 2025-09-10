import React from 'react';

const AttackList = ({ attacks }) => {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    return `${diffDays}d ago`;
  };

  const getProtocolColor = (protocol) => {
    const colors = {
      'TCP': 'bg-blue-500',
      'UDP': 'bg-green-500',
      'HTTP': 'bg-yellow-500',
      'HTTPS': 'bg-orange-500',
      'SSH': 'bg-purple-500',
      'FTP': 'bg-pink-500',
      'SMTP': 'bg-indigo-500'
    };
    return colors[protocol] || 'bg-gray-500';
  };

  const getPortColor = (port) => {
    if (port === 22) return 'text-green-400'; // SSH
    if (port === 80) return 'text-blue-400'; // HTTP
    if (port === 443) return 'text-yellow-400'; // HTTPS
    if (port === 3389) return 'text-red-400'; // RDP
    if (port === 5432) return 'text-purple-400'; // PostgreSQL
    if (port === 3306) return 'text-orange-400'; // MySQL
    return 'text-gray-400';
  };

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h3 className="text-lg font-bold text-white">Recent Attacks</h3>
        <p className="text-sm text-gray-400">{attacks.length} total attacks</p>
      </div>
      
      <div className="flex-1 overflow-y-auto">
        {attacks.length === 0 ? (
          <div className="p-4 text-center text-gray-400">
            <div className="text-4xl mb-2">🛡️</div>
            <div>No attacks detected yet</div>
            <div className="text-sm mt-1">Waiting for malicious activity...</div>
          </div>
        ) : (
          <div className="space-y-2 p-2">
            {attacks.map((attack, index) => (
              <div 
                key={`${attack.id}-${index}`} 
                className="recent-attack bg-gray-700 rounded-lg p-3 hover:bg-gray-600 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-red-400 text-lg">🚨</span>
                    <span className="font-mono text-sm font-bold text-white">
                      {attack.ip_address}
                    </span>
                  </div>
                  <span className="text-xs text-gray-400">
                    {formatTime(attack.timestamp)}
                  </span>
                </div>
                
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded text-xs font-bold ${getProtocolColor(attack.protocol)}`}>
                      {attack.protocol}
                    </span>
                    <span className={`font-mono ${getPortColor(attack.port)}`}>
                      :{attack.port}
                    </span>
                  </div>
                  
                  <div className="text-gray-400 text-xs">
                    {attack.city}, {attack.country}
                  </div>
                </div>
                
                {attack.country === 'Unknown' && (
                  <div className="mt-1 text-xs text-yellow-400">
                    ⚠️ Location unknown
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default AttackList;
