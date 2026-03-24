import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react";

const config = defineConfig({
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#e8f5ec" },
          100: { value: "#c6e6ce" },
          200: { value: "#a0d4ad" },
          300: { value: "#78c18b" },
          400: { value: "#58b271" },
          500: { value: "#34964a" },
          600: { value: "#2a7e3b" },
          700: { value: "#1f6330" },
          800: { value: "#154a23" },
          900: { value: "#0b3116" },
        },
      },
    },
  },
});

export const system = createSystem(defaultConfig, config);
