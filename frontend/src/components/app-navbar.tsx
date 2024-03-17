import {
  AppBar,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import { uiValues } from "@/constants";
import { useAppDispatch, useAppSelector } from "@/store";
import { closeDrawer, openDrawer } from "@/store/features/shared";
import { AccountCircle } from "@mui/icons-material";
import { MouseEvent, useState } from "react";
import { logoutUser } from "@/store/features/auth";

const AppNavbar = () => {
  // redux
  const { drawer, title } = useAppSelector((state) => state.shared);
  const { isAuthenticate } = useAppSelector((state) => state.auth);
  const dispatch = useAppDispatch();

  // states
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  // methods
  const handleDrawerToggle = () => {
    if (drawer) {
      dispatch(closeDrawer());
    } else {
      dispatch(openDrawer());
    }
  };

  const logout = () => {
    dispatch(logoutUser());
  };

  const handleMenu = (event: MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };
  return (
    <AppBar
      position="fixed"
      sx={{
        width: { sm: `calc(100% - ${uiValues.drawerWidth}px)` },
        ml: { sm: `${uiValues.drawerWidth}px` },
      }}
    >
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="abrir menu"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{ mr: 2, display: { sm: "none" } }}
        >
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" noWrap component="div">
          {/* {title} */}
        </Typography>

        {isAuthenticate && (
          <Box sx={{ marginLeft: "auto" }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleMenu}
              color="inherit"
            >
              <AccountCircle />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorEl}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              open={Boolean(anchorEl)}
              onClose={handleClose}
            >
              <MenuItem onClick={() => logout()}>Cerrar sesión</MenuItem>
            </Menu>
          </Box>
        )}
      </Toolbar>
    </AppBar>
  );
};

export default AppNavbar;
