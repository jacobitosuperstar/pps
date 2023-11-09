import { uiValues } from "@/constants";
import {
  Box,
  Divider,
  Drawer,
  List,
  ListItem,
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
import { useAppDispatch, useAppSelector } from "@/store";
import { closeDrawer, openDrawer } from "@/store/features/shared";

const AppDrawerList = () => {
  const menuList = [
    { label: "Dashboard", icon: <PieChartIcon /> },
    { label: "Personal", icon: <PeopleIcon /> },
    { label: "Programación", icon: <AccessAlarmIcon /> },
    { label: "Produción", icon: <PrecisionManufacturingIcon /> },
  ];

  return (
    <>
      <Toolbar>
        <Typography variant="h5" textAlign="center" component="h1" fontWeight="700">
          PPS
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuList.map((item, index) => (
          <ListItem key={item.label} disablePadding>
            <ListItemButton>
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
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
