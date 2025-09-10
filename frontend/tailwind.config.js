/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'attack-red': '#ef4444',
        'attack-orange': '#f97316',
        'attack-yellow': '#eab308',
      }
    },
  },
  plugins: [],
}
