import { useEffect, useState } from "react";
import type { ReactNode } from "react";
import { ColorModeContext } from "./color-mode-context";

type ColorMode = "light" | "dark";

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
