import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import Home from "../pages/Home";

export const HomeRoute: RouteObject = {
  path: PATHS.HOME,
  element: <Home />,
};
