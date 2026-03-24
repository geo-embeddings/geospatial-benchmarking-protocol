import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

type ColorMode = "light" | "dark";

interface ColorModeContextValue {
  colorMode: ColorMode;
  toggleColorMode: () => void;
}

const ColorModeContext = createContext<ColorModeContextValue>({
  colorMode: "light",
  toggleColorMode: () => {},
});

function getSystemPreference(): ColorMode {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function getInitialColorMode(): ColorMode {
  const stored = localStorage.getItem("color-mode");
  if (stored === "light" || stored === "dark") return stored;
  return getSystemPreference();
}

export function ColorModeProvider({ children }: { children: ReactNode }) {
  const [colorMode, setColorMode] = useState<ColorMode>(getInitialColorMode);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", colorMode === "dark");
    localStorage.setItem("color-mode", colorMode);
  }, [colorMode]);

  function toggleColorMode() {
    setColorMode((prev) => (prev === "light" ? "dark" : "light"));
  }

  return (
    <ColorModeContext.Provider value={{ colorMode, toggleColorMode }}>
      {children}
    </ColorModeContext.Provider>
  );
}

export function useColorMode() {
  return useContext(ColorModeContext);
}
