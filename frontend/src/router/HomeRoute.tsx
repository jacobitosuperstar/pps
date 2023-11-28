import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import Home from "../pages/Home";
import { AuthenticationValidator } from "@/components";
import { MainLayout } from "@/layouts";

export const HomeRoute: RouteObject = {
  element: <AuthenticationValidator />,
  children: [
    {
      element: (
        <MainLayout>
          <Home />
        </MainLayout>
      ),
      path: PATHS.HOME,
    },
  ],
};
