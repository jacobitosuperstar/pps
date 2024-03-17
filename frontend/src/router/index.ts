import { createBrowserRouter } from "react-router-dom";
import { HomeRoute } from "./home.route";
import { LoginRoute } from "./login.route";
import { EmployeesRoute } from "./employees.route";
import { MachinesRoute } from "./machines.route";

export const router = createBrowserRouter([
  HomeRoute,
  LoginRoute,
  EmployeesRoute,
  MachinesRoute,
]);
