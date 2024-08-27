/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-purple': '#282829', // Really dark purple
        'dark-blue': '#0f172a',   // Darker than blue-900
      },
    },
  },
  plugins: [],
}


