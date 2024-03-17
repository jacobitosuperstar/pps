import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import { AuthenticationValidator } from "@/components";
import { MainLayout } from "@/layouts";
import MachinesPage from "@/pages/machines/machines.page";

export const MachinesRoute: RouteObject = {
  element: <AuthenticationValidator />,
  children: [
    {
      element: (
        <MainLayout>
          <MachinesPage />
        </MainLayout>
      ),
      path: PATHS.MACHINES,
    },
  ],
};
