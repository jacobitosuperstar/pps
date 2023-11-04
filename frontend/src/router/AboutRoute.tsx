import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import About from "../pages/About";

export const AboutRoute: RouteObject = {
  path: PATHS.ABOUT,
  element: <About />,
};
