import { PATHS } from "@/constant/paths";
import { lazy } from "react";
import type { RouteObject } from "react-router-dom";
import { ProtectedPage } from "@/components/protected-page";
import { Layout } from "@/components/layout/layout";

const OooListPage = lazy(() => import("./pages/ooo-list-page"));
const CreateOooPage = lazy(() => import("./pages/create-ooo-page"));
const UpdateOooPage = lazy(() => import("./pages/update-ooo-page"));

export const oooRouter: RouteObject = {
  element: (
    <ProtectedPage>
      <Layout />
    </ProtectedPage>
  ),
  children: [
    {
      path: PATHS.OOO.INDEX,
      element: <OooListPage />,
    },
    {
      path: PATHS.OOO.CREATE,
      element: <CreateOooPage />,
    },
    {
      path: PATHS.OOO.EDIT,
      element: <UpdateOooPage />,
    },
  ],
};
