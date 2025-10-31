import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        typhoon: {
          primary: "#726bdf",
          dark: "#28204b",
          darker: "#313131",
        },
        lavender: {
          DEFAULT: "#a77be8",
          light: "#c299f0",
          dark: "#8d5ed4",
        },
        kobi: {
          DEFAULT: "#e19ec8",
          light: "#f0bfdd",
          dark: "#d486b4",
        },
        rhythm: {
          DEFAULT: "#7c7399",
          light: "#9b90b3",
          dark: "#5e5577",
        },
        cerulean: {
          DEFAULT: "#6ca1c7",
          light: "#8bb9d9",
          dark: "#5188b0",
        },
        desert: {
          DEFAULT: "#f0bfaa",
          light: "#f8dccb",
          dark: "#e6a88f",
        },
      },
      backgroundImage: {
        "typhoon-gradient": "linear-gradient(135deg, #726bdf 0%, #a77be8 100%)",
        "typhoon-gradient-dark": "linear-gradient(135deg, #28204b 0%, #313131 100%)",
      },
      backgroundSize: {
        "size-200": "200% 100%",
      },
      backgroundPosition: {
        "pos-0": "0% 0%",
        "pos-100": "100% 0%",
      },
    },
  },
  plugins: [],
};

export default config;

