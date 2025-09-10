import React from 'react';

const FilterPanel = ({ filters, onFilterChange, onClearFilters }) => {
  const countries = [
    'United States', 'China', 'Russia', 'Germany', 'United Kingdom',
    'France', 'Japan', 'Brazil', 'India', 'Canada', 'Australia',
    'South Korea', 'Italy', 'Spain', 'Netherlands', 'Poland',
    'Ukraine', 'Turkey', 'Iran', 'Israel'
  ];

  const protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'SSH', 'FTP', 'SMTP'];

  const timeRanges = [
    { value: '1h', label: 'Last Hour' },
    { value: '24h', label: 'Last 24 Hours' },
    { value: '7d', label: 'Last 7 Days' },
    { value: '30d', label: 'Last 30 Days' },
    { value: 'all', label: 'All Time' }
  ];

  const hasActiveFilters = filters.country || filters.protocol || filters.timeRange !== '24h';

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-bold text-white">Filters</h3>
        {hasActiveFilters && (
          <button
            onClick={onClearFilters}
            className="text-xs bg-red-600 hover:bg-red-700 px-2 py-1 rounded transition-colors"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Country Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Country
        </label>
        <select
          value={filters.country}
          onChange={(e) => onFilterChange({ country: e.target.value })}
          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Countries</option>
          {countries.map(country => (
            <option key={country} value={country}>{country}</option>
          ))}
        </select>
      </div>

      {/* Protocol Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Protocol
        </label>
        <select
          value={filters.protocol}
          onChange={(e) => onFilterChange({ protocol: e.target.value })}
          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Protocols</option>
          {protocols.map(protocol => (
            <option key={protocol} value={protocol}>{protocol}</option>
          ))}
        </select>
      </div>

      {/* Time Range Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-1">
          Time Range
        </label>
        <select
          value={filters.timeRange}
          onChange={(e) => onFilterChange({ timeRange: e.target.value })}
          className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {timeRanges.map(range => (
            <option key={range.value} value={range.value}>{range.label}</option>
          ))}
        </select>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters && (
        <div className="bg-gray-700 rounded-lg p-3">
          <div className="text-sm font-medium text-gray-300 mb-2">Active Filters:</div>
          <div className="flex flex-wrap gap-2">
            {filters.country && (
              <span className="bg-blue-600 text-white px-2 py-1 rounded text-xs">
                Country: {filters.country}
              </span>
            )}
            {filters.protocol && (
              <span className="bg-green-600 text-white px-2 py-1 rounded text-xs">
                Protocol: {filters.protocol}
              </span>
            )}
            {filters.timeRange !== '24h' && (
              <span className="bg-yellow-600 text-white px-2 py-1 rounded text-xs">
                Time: {timeRanges.find(r => r.value === filters.timeRange)?.label}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterPanel;
