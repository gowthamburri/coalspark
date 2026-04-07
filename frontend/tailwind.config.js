/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand palette
        coal: {
          50:  '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          800: '#1a1a1a',
          900: '#0f0f0f',
          950: '#080808',
        },
        ember: {
          50:  '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#ff6b00',   // Primary brand orange
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
        },
        ash: {
          100: '#2a2a2a',
          200: '#222222',
          300: '#1e1e1e',
          400: '#1a1a1a',
          500: '#161616',
        },
      },
      fontFamily: {
        poppins: ['Poppins', 'sans-serif'],
        sans: ['Poppins', 'sans-serif'],
      },
      backgroundImage: {
        'ember-glow': 'radial-gradient(ellipse at center, rgba(255,107,0,0.15) 0%, transparent 70%)',
        'coal-gradient': 'linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%)',
      },
      animation: {
        'fade-in': 'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-in-right': 'slideInRight 0.35s ease-out',
        'pulse-ember': 'pulseEmber 2s ease-in-out infinite',
        'shimmer': 'shimmer 1.5s infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInRight: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0)' },
        },
        pulseEmber: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(255,107,0,0.3)' },
          '50%': { boxShadow: '0 0 40px rgba(255,107,0,0.6)' },
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      boxShadow: {
        'ember': '0 0 20px rgba(255, 107, 0, 0.3)',
        'ember-lg': '0 0 40px rgba(255, 107, 0, 0.4)',
        'card': '0 4px 24px rgba(0, 0, 0, 0.4)',
        'card-hover': '0 8px 40px rgba(0, 0, 0, 0.6)',
      },
    },
  },
  plugins: [],
}