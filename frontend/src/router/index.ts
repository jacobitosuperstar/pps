import { createBrowserRouter } from "react-router-dom";
import { AboutRoute } from "./AboutRoute";
import { HomeRoute } from "./HomeRoute";
import { LoginRoute } from "./LoginRoute";

export const router = createBrowserRouter([HomeRoute, AboutRoute, LoginRoute]);
