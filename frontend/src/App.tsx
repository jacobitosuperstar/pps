import { RouterProvider } from "react-router-dom";
import { ThemeProvider } from "@emotion/react";
import { CssBaseline } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { router } from "./router";
import theme from "./theme";
import { Provider } from "react-redux";
import { store } from "./store";
import { SnackbarProvider } from "notistack";
import { ConfirmProvider } from "material-ui-confirm";
import "dayjs/locale/es";

const App = () => {
  return (
    <>
      <Provider store={store}>
        <ThemeProvider theme={theme}>
          <LocalizationProvider adapterLocale="es" dateAdapter={AdapterDayjs}>
            <ConfirmProvider>
              <SnackbarProvider autoHideDuration={7000}>
                <CssBaseline />
                <RouterProvider router={router} />;
              </SnackbarProvider>
            </ConfirmProvider>
          </LocalizationProvider>
        </ThemeProvider>
      </Provider>
    </>
  );
};

export default App;
