import { PATHS } from "@/constant/paths";
import { lazy } from "react";
import type { RouteObject } from "react-router-dom";
import { ProtectedPage } from "@/components/protected-page";
import { Layout } from "@/components/layout/layout";

const EmployeesPage = lazy(() => import("./pages/employees-page"));
const CreateEmployeePage = lazy(() => import("./pages/create-employee-page"));
const UpdateEmployeePage = lazy(() => import("./pages/update-employee-page"));

export const employeesRouter: RouteObject = {
  element: (
    <ProtectedPage>
      <Layout />
    </ProtectedPage>
  ),
  children: [
    {
      path: PATHS.EMPLOYEES.INDEX,
      element: <EmployeesPage />,
    },
    {
      path: PATHS.EMPLOYEES.CREATE,
      element: <CreateEmployeePage />,
    },
    {
      path: PATHS.EMPLOYEES.EDIT,
      element: <UpdateEmployeePage />,
    },
  ],
};
