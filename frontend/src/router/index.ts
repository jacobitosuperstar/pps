import { createBrowserRouter } from "react-router-dom";
import { HomeRoute } from "./HomeRoute";
import { LoginRoute } from "./LoginRoute";
import { EmployeesRoute } from "./EmployeesRoute";

export const router = createBrowserRouter([
  HomeRoute,
  LoginRoute,
  EmployeesRoute,
]);
