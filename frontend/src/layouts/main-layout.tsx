import { AppDrawer, AppNavbar } from "@/components";
import { uiValues } from "@/constants";
import { Box, Toolbar } from "@mui/material";
import { FC, ReactElement } from "react";
import { Outlet } from "react-router-dom";

interface Props {
  children?: ReactElement;
}

const MainLayout: FC<Props> = ({ children }) => {
  return (
    <Box sx={{ display: "flex" }}>
      <AppNavbar></AppNavbar>
      <AppDrawer></AppDrawer>

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${uiValues.drawerWidth}px)` },
        }}
      >
        <Toolbar />
        {children || <Outlet></Outlet>}
      </Box>
    </Box>
  );
};

export default MainLayout;
