import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import Login from "../pages/Login";

export const LoginRoute: RouteObject = {
  path: PATHS.LOGIN,
  element: <Login />,
};
