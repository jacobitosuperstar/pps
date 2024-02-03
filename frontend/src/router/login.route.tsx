import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import LoginPage from "../pages/login/login.page";

export const LoginRoute: RouteObject = {
  path: PATHS.LOGIN,
  element: <LoginPage />,
};
