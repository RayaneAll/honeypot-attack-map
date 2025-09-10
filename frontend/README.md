# 🛡️ Honeypot Attack Map - Frontend

Interface web moderne pour la visualisation en temps réel des attaques détectées par le honeypot.

## 🎯 Vue d'ensemble

Ce frontend fournit :
- **Carte interactive** avec Leaflet.js pour visualiser les attaques
- **Liste temps réel** des attaques récentes
- **WebSocket** pour les mises à jour en direct
- **Filtres avancés** par pays, protocole, port, période
- **Mode sombre** avec TailwindCSS
- **Interface responsive** pour tous les écrans

## 🏗️ Architecture

```
frontend/
├── src/
│   ├── components/
│   │   ├── AttackMap.jsx      # Carte Leaflet avec points d'attaque
│   │   ├── AttackList.jsx     # Liste des attaques récentes
│   │   └── Navbar.jsx         # Barre de navigation
│   ├── pages/
│   │   └── Dashboard.jsx      # Page principale
│   ├── services/
│   │   ├── api.js             # Service API REST
│   │   └── websocket.js       # Service WebSocket
│   ├── App.jsx                # Composant principal
│   └── main.jsx               # Point d'entrée
├── index.html                 # Template HTML
├── tailwind.config.js         # Configuration TailwindCSS
└── package.json               # Dépendances
```

## 🚀 Installation et Démarrage

### Prérequis
- Node.js 18+
- npm ou yarn
- Backend API en cours d'exécution

### Installation

1. **Installer les dépendances**
```bash
npm install
# ou
yarn install
```

2. **Configurer l'environnement**
```bash
cp .env.example .env
# Modifier les URLs si nécessaire
```

3. **Lancer en développement**
```bash
npm run dev
# ou
yarn dev
```

4. **Accéder à l'application**
- URL : http://localhost:3000
- L'application se connecte automatiquement au backend sur le port 8000

### Build de production

```bash
npm run build
# ou
yarn build
```

## 🎨 Fonctionnalités

### Carte Interactive (AttackMap)
- **Points d'attaque** avec couleurs selon le niveau de risque
- **Popup détaillé** avec informations complètes
- **Animation pulse** pour les nouvelles attaques
- **Zoom et déplacement** libre
- **Légende** et statistiques en overlay

### Liste des Attaques (AttackList)
- **Affichage temps réel** des attaques
- **Animation d'apparition** pour les nouvelles attaques
- **Informations détaillées** : IP, port, protocole, localisation
- **Auto-scroll** vers les nouvelles attaques
- **Pagination** automatique

### Navigation (Navbar)
- **Statut de connexion** en temps réel
- **Compteur d'attaques** total
- **Heure actuelle** mise à jour
- **Bouton mode sombre** avec persistance
- **Design responsive**

### Filtres Avancés
- **Par pays** : Liste déroulante avec statistiques
- **Par protocole** : TCP, UDP, HTTP, HTTPS, SSH, etc.
- **Par port** : Recherche par numéro de port
- **Par période** : 1h, 24h, 1 semaine, 1 mois, tout
- **Réinitialisation** des filtres

### Mode Sombre
- **Basculement** via le bouton dans la navbar
- **Persistance** dans le localStorage
- **Thème cohérent** sur tous les composants
- **Couleurs optimisées** pour la cybersécurité

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` :
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_TITLE=Honeypot Attack Map
VITE_APP_VERSION=1.0.0
```

### Configuration TailwindCSS

Le fichier `tailwind.config.js` contient :
- **Couleurs personnalisées** pour le thème cybersécurité
- **Animations** pour les effets d'attaque
- **Mode sombre** configuré
- **Classes utilitaires** personnalisées

### Configuration Vite

Le fichier `vite.config.js` configure :
- **Proxy API** vers le backend
- **Proxy WebSocket** pour le temps réel
- **Build optimisé** avec sourcemaps
- **Port de développement** : 3000

## 📡 Communication avec le Backend

### API REST
```javascript
import { attackService } from './services/api';

// Récupérer les attaques
const attacks = await attackService.getAttacks({
  limit: 100,
  country: 'United States',
  protocol: 'SSH'
});

// Récupérer les statistiques
const stats = await attackService.getStats();
```

### WebSocket
```javascript
import webSocketService from './services/websocket';

// Connexion
webSocketService.connect();

// Écouter les nouvelles attaques
webSocketService.on('new_attack', (attack) => {
  console.log('Nouvelle attaque:', attack);
});
```

## 🎨 Composants

### AttackMap
```jsx
<AttackMap
  attacks={attacks}           // Attaques existantes
  newAttacks={newAttacks}     // Nouvelles attaques
  className="h-full"          // Classes CSS
/>
```

### AttackList
```jsx
<AttackList
  attacks={attacks}           // Attaques existantes
  newAttacks={newAttacks}     // Nouvelles attaques
  onAttackClick={handler}     // Callback de clic
  maxItems={50}               // Nombre max d'éléments
  className="h-full"          // Classes CSS
/>
```

### Navbar
```jsx
<Navbar
  isConnected={isConnected}   // Statut de connexion
  attackCount={totalAttacks}  // Nombre d'attaques
  onToggleDarkMode={handler}  // Callback mode sombre
  isDarkMode={isDarkMode}     // État du mode sombre
/>
```

## 🎯 Niveaux de Risque

### Ports Critiques (Rouge)
- **22** : SSH
- **3389** : RDP
- **5432** : PostgreSQL
- **3306** : MySQL
- **1433** : MSSQL

### Ports Élevés (Orange)
- **21** : FTP
- **23** : Telnet
- **25** : SMTP
- **53** : DNS
- **80** : HTTP
- **443** : HTTPS
- **993** : IMAPS
- **995** : POP3S

### Ports Faibles (Vert)
- Tous les autres ports

## 📱 Responsive Design

### Breakpoints TailwindCSS
- **sm** : 640px et plus
- **md** : 768px et plus
- **lg** : 1024px et plus
- **xl** : 1280px et plus

### Adaptations
- **Mobile** : Layout vertical, cartes empilées
- **Tablet** : Layout hybride, filtres compacts
- **Desktop** : Layout horizontal, toutes les fonctionnalités

## 🧪 Tests et Développement

### Mode Développement
```bash
npm run dev
```

### Linting
```bash
npm run lint
```

### Build de production
```bash
npm run build
```

### Preview de production
```bash
npm run preview
```

## 🐛 Dépannage

### Problèmes Courants

#### L'application ne se connecte pas au backend
```bash
# Vérifier que le backend est en cours d'exécution
curl http://localhost:8000/health

# Vérifier les variables d'environnement
cat .env
```

#### WebSocket ne fonctionne pas
```bash
# Vérifier la connexion WebSocket
wscat -c ws://localhost:8000/ws
```

#### Erreurs de build
```bash
# Nettoyer et réinstaller
rm -rf node_modules package-lock.json
npm install
```

#### Problèmes de styles
```bash
# Rebuilder TailwindCSS
npm run build
```

### Logs de Débogage

Activer les logs dans la console :
```javascript
// Dans le service API
console.log('🚀 API Request:', config);

// Dans le service WebSocket
console.log('🔌 WebSocket connecté');
```

## 📊 Performance

### Optimisations Incluses
- **Lazy loading** des composants
- **Memoization** des calculs coûteux
- **Debouncing** des filtres
- **Virtualisation** de la liste des attaques
- **Compression** des assets

### Métriques
- **First Contentful Paint** : < 1.5s
- **Largest Contentful Paint** : < 2.5s
- **Cumulative Layout Shift** : < 0.1
- **Time to Interactive** : < 3s

## 🔒 Sécurité

### Bonnes Pratiques
- **Validation** des données reçues
- **Sanitisation** des entrées utilisateur
- **HTTPS** en production
- **CSP** (Content Security Policy) configuré

### Configuration Sécurisée
```javascript
// Headers de sécurité
const securityHeaders = {
  'Content-Security-Policy': "default-src 'self'",
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff'
};
```

## 📚 Ressources

### Documentation
- [React](https://reactjs.org/docs)
- [Vite](https://vitejs.dev/guide)
- [TailwindCSS](https://tailwindcss.com/docs)
- [Leaflet](https://leafletjs.com/reference.html)
- [Socket.IO](https://socket.io/docs)

### Outils de Développement
- [React Developer Tools](https://reactjs.org/blog/2019/08/15/new-react-devtools.html)
- [Tailwind CSS IntelliSense](https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss)
- [ESLint](https://eslint.org/)

## 🤝 Contribution

### Structure du Code
- **Composants** : `src/components/`
- **Pages** : `src/pages/`
- **Services** : `src/services/`
- **Styles** : `src/index.css`

### Conventions
- **Nommage** : PascalCase pour les composants
- **Props** : camelCase
- **Événements** : onEventName
- **Classes CSS** : TailwindCSS + classes personnalisées

### Ajout de Fonctionnalités
1. Créer le composant dans `src/components/`
2. Ajouter les tests si nécessaire
3. Documenter les props et l'utilisation
4. Mettre à jour ce README

## 📝 Changelog

### Version 1.0.0
- Carte interactive avec Leaflet.js
- Liste des attaques en temps réel
- WebSocket pour les mises à jour
- Filtres avancés
- Mode sombre
- Interface responsive
- Thème cybersécurité

## 📞 Support

Pour toute question ou problème :
- Consulter la documentation
- Vérifier les logs de la console
- Tester la connexion au backend
- Ouvrir une issue sur GitHub

---

**⚡ Développé avec React, Vite, TailwindCSS et Leaflet.js pour la cybersécurité**
