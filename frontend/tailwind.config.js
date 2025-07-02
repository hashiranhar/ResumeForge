/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{html,js,svelte,ts}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
        },
        // Simplified dark theme colors
        dark: {
          50: "#181818",
          100: "#181818",
          200: "#181818",
          300: "#181818",
          400: "#181818",
          500: "#181818",
          600: "#181818",
          700: "#181818",
          800: "#181818",
          900: "#000000",
        },
      },
    },
  },
  plugins: [],
};
