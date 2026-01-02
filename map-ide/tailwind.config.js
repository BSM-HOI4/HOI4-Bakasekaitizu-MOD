/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'ide-bg': '#1e1e1e',
        'ide-sidebar': '#252526',
        'ide-panel': '#2d2d30',
        'ide-border': '#3c3c3c',
        'ide-text': '#cccccc',
        'ide-text-muted': '#808080',
        'ide-accent': '#007acc',
        'ide-accent-hover': '#1c97ea',
        'ide-selection': '#264f78',
        'ide-highlight': '#ffcc00',
      },
      fontFamily: {
        mono: ['Consolas', 'Monaco', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
};
