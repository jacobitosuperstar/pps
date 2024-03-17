import { PATHS, uiValues } from "@/constants";
import {
  Box,
  Divider,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from "@mui/material";
import PieChartIcon from "@mui/icons-material/PieChart";
import PeopleIcon from "@mui/icons-material/People";
import AccessAlarmIcon from "@mui/icons-material/AccessAlarm";
import PrecisionManufacturingIcon from "@mui/icons-material/PrecisionManufacturing";
import ArticleIcon from "@mui/icons-material/Article";
import { useAppDispatch, useAppSelector } from "@/store";
import { closeDrawer, openDrawer } from "@/store/features/shared";
import { Link, useLocation } from "react-router-dom";

const AppDrawerList = () => {
  const location = useLocation();
  // state
  const menuList = [
    { label: "Dashboard", icon: <PieChartIcon />, to: PATHS.HOME },
    { label: "Personal", icon: <PeopleIcon />, to: PATHS.EMPLOYEES },
    { label: "Permisos", icon: <ArticleIcon />, to: PATHS.OOO },
    // { label: "Programación", icon: <AccessAlarmIcon />, to: PATHS.HOME },
    {
      label: "Tipos de maquinas",
      icon: <PrecisionManufacturingIcon />,
      to: PATHS.MACHINES,
    },
  ];

  return (
    <>
      <Toolbar>
        <Typography
          variant="h5"
          textAlign="center"
          component="h1"
          fontWeight="700"
        >
          PPS
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuList.map((item) => (
          <ListItemButton
            selected={location.pathname === item.to}
            component={Link}
            to={item.to}
            key={item.label}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </>
  );
};

const AppDrawer = () => {
  // redux
  const drawer = useAppSelector((state) => state.shared.drawer);
  const dispatch = useAppDispatch();

  // methods
  const handleDrawerToggle = () => {
    if (drawer) {
      dispatch(closeDrawer());
    } else {
      dispatch(openDrawer());
    }
  };
  return (
    <Box
      component="nav"
      sx={{ width: { sm: uiValues.drawerWidth }, flexShrink: { sm: 0 } }}
      aria-label="Menu items"
    >
      <Drawer
        variant="temporary"
        open={drawer}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true, // Better open performance on mobile.
        }}
        sx={{
          display: { xs: "block", sm: "none" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: uiValues.drawerWidth,
          },
        }}
      >
        <AppDrawerList />
      </Drawer>
      <Drawer
        variant="permanent"
        sx={{
          display: { xs: "none", sm: "block" },
          "& .MuiDrawer-paper": {
            boxSizing: "border-box",
            width: uiValues.drawerWidth,
          },
        }}
        open
      >
        <AppDrawerList />
      </Drawer>
    </Box>
  );
};

export default AppDrawer;
