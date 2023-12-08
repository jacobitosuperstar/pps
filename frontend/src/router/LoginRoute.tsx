import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import LoginPage from "../pages/Login";

export const LoginRoute: RouteObject = {
  path: PATHS.LOGIN,
  element: <LoginPage />,
};
