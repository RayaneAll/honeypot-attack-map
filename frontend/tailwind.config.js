/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Couleurs personnalisées pour le thème cybersécurité
        'attack-red': '#ef4444',
        'attack-orange': '#f97316',
        'attack-yellow': '#eab308',
        'attack-green': '#22c55e',
        'attack-blue': '#3b82f6',
        'attack-purple': '#a855f7',
        'dark-bg': '#0f172a',
        'dark-card': '#1e293b',
        'dark-border': '#334155',
      },
      animation: {
        'pulse-attack': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-attack': 'bounce 1s infinite',
        'ping-attack': 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
      },
      keyframes: {
        'pulse-attack': {
          '0%, 100%': {
            opacity: '1',
            transform: 'scale(1)',
          },
          '50%': {
            opacity: '0.8',
            transform: 'scale(1.1)',
          },
        }
      }
    },
  },
  plugins: [],
  darkMode: 'class',
}