/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{vue,js}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3B82F6',
        secondary: '#10B981',
        accent: '#0bf5ed',
        dark: '#1F2937',
      },
      fontSize: {
        'heading': '2.5rem',
        'subheading': '1.5rem',
      },
      fontFamily: {
        'blender': ['BlenderPro', 'sans-serif'],
      },
    },
  },
  plugins: [],
}