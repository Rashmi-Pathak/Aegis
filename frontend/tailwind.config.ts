import type { Config } from 'tailwindcss';

export default {
  darkMode: ['class'],
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          primary: '#080604',
          secondary: '#0D0906',
          surface: '#120C08',
          elevated: '#17100B',
          card: 'rgba(18, 12, 8, 0.75)',
        },
        aegis: {
          orange: '#FF6A00',
          'orange-bright': '#FF8A24',
          'orange-hot': '#FFB15A',
          'orange-dark': '#B84200',
          'text-primary': '#F5F0EA',
          'text-secondary': '#A89D92',
          'text-muted': '#6F665F',
          border: 'rgba(255, 106, 0, 0.18)',
          'border-bright': 'rgba(255, 106, 0, 0.42)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Geist', 'Manrope', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
        script: ['"Alex Brush"', 'cursive'],
        editorial: ['"Instrument Serif"', '"Playfair Display"', 'serif'],
        fullwidth: ['"Space Grotesk"', 'monospace'],
      },
      boxShadow: {
        'glow-sm': '0 0 15px rgba(255, 106, 0, 0.15)',
        'glow-md': '0 0 25px rgba(255, 106, 0, 0.25)',
        'glow-lg': '0 0 40px rgba(255, 106, 0, 0.35)',
        'glow-hot': '0 0 50px rgba(255, 177, 90, 0.45)',
        card: '0 0 0 1px rgba(255,106,0,0.14), 0 20px 60px rgba(0,0,0,0.45)',
        'card-hover': '0 0 0 1px rgba(255,106,0,0.45), 0 0 30px rgba(255,106,0,0.22), 0 20px 60px rgba(0,0,0,0.6)',
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float-slow': 'float 6s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
} satisfies Config;
