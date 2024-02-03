import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import HomePage from "../pages/home/home.page";
import { AuthenticationValidator } from "@/components";
import { MainLayout } from "@/layouts";

export const HomeRoute: RouteObject = {
  element: <AuthenticationValidator />,
  children: [
    {
      element: (
        <MainLayout>
          <HomePage />
        </MainLayout>
      ),
      path: PATHS.HOME,
    },
  ],
};
