import type { RouteObject } from "react-router-dom";
import { PATHS } from "../constants";
import { AuthenticationValidator } from "@/components";
import { MainLayout } from "@/layouts";
import EmployeesPage from "@/pages/employees/employee.page";
import OooPage from "@/pages/ooo/ooo.page";

export const EmployeesRoute: RouteObject = {
  element: <AuthenticationValidator />,
  children: [
    {
      element: (
        <MainLayout>
          <EmployeesPage />
        </MainLayout>
      ),
      path: PATHS.EMPLOYEES,
    },
    {
      element: (
        <MainLayout>
          <OooPage />
        </MainLayout>
      ),
      path: PATHS.OOO,
    },
  ],
};
