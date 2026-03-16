/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      /* Theme colors come from style.css @theme (CSS variables). Only non-theme utilities below. */
      borderRadius: {
        card: '12px',
        button: '10px',
      },
      boxShadow: {
        card: '0 4px 10px rgba(0,0,0,0.08)',
        'card-hover': '0 6px 14px rgba(0,0,0,0.1)',
      },
    },
  },
  plugins: [],
}
