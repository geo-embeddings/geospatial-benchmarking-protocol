import { useContext } from "react";
import { ColorModeContext } from "./color-mode-context";

export function useColorMode() {
  return useContext(ColorModeContext);
}
