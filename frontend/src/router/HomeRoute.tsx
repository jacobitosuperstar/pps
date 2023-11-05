import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import Home from "../pages/Home";
import { AuthenticationValidator } from "@/components";

export const HomeRoute: RouteObject = {
  element: <AuthenticationValidator />,
  children: [
    {
      element: <Home />,
      path: PATHS.HOME,
    },
  ],
};
