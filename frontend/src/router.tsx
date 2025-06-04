import { createBrowserRouter } from "react-router-dom";
import { PATHS } from "./constant/paths";
import LoginPage from "./pages/login/login-page";
import HomePage from "./pages/home/home-page";
import { ProtectedPage } from "./components/protected-page";
import { Layout } from "./components/layout/layout";
import { lazy } from "react";

const EmployeesPage = lazy(() => import("./pages/employees/employees-page"));
const CreateEmployeePage = lazy(
  () => import("./pages/employees/create-employee-page")
);

export const router = createBrowserRouter([
  {
    path: PATHS.LOGIN,
    element: <LoginPage />,
  },
  {
    element: (
      <ProtectedPage>
        <Layout />
      </ProtectedPage>
    ),
    children: [
      {
        path: PATHS.HOME,
        element: <HomePage />,
      },
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
        element: <EmployeesPage />,
      },
    ],
  },
]);
