import { Navigate, Outlet } from "react-router-dom";
import { useAppSelector } from "../store/store";
import { FC, ReactElement } from "react";
import { PATHS } from "@/constants";

interface Props {
  children?: ReactElement;
}

const AuthenticationValidator: FC<Props> = ({ children }) => {
  const isAuthenticate = useAppSelector((state) => state.auth.isAuthenticate);

  if (!isAuthenticate) {
    return <Navigate to={PATHS.LOGIN}></Navigate>;
  }

  if (children) return children;

  return <Outlet></Outlet>;
};

export default AuthenticationValidator;
