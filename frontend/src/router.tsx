import { createBrowserRouter } from "react-router-dom";
import { PATHS } from "./constant/paths";
import { ProtectedPage } from "./components/protected-page";
import { Layout } from "./components/layout/layout";
import { employeesRouter } from "./modules/employees/router";
import LoginPage from "./modules/login/login-page";
import HomePage from "./modules/home/home-page";
import { oooRouter } from "./modules/ooo/router";

export const router = createBrowserRouter([
  {
    path: PATHS.LOGIN,
    element: <LoginPage />,
  },
  employeesRouter,
  oooRouter,
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
    ],
  },
]);
