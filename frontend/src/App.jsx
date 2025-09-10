/**
 * Composant principal App
 * Point d'entrée de l'application React
 */

import React from 'react';
import Dashboard from './pages/Dashboard';
import './index.css';

function App() {
  return (
    <div className="App">
      <Dashboard />
    </div>
  );
}

export default App;
