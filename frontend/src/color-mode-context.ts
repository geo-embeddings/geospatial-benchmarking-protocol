import { createContext } from "react";

type ColorMode = "light" | "dark";

export interface ColorModeContextValue {
  colorMode: ColorMode;
  toggleColorMode: () => void;
}

export const ColorModeContext = createContext<ColorModeContextValue>({
  colorMode: "light",
  toggleColorMode: () => {},
});
