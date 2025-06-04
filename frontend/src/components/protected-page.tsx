import { PATHS } from "@/constant/paths";
import { useAppSelector } from "@/store/store";
import { Navigate, Outlet } from "react-router-dom";

export const ProtectedPage = ({ children }: { children?: React.ReactNode }) => {
  const isAuthenticate = useAppSelector((state) => state.auth.isAuthenticate);

  if (!isAuthenticate) {
    return <Navigate to={PATHS.LOGIN}></Navigate>;
  }

  if (children) return children;

  return <Outlet></Outlet>;
};
