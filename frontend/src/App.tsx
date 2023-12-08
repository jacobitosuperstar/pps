import { RouterProvider } from "react-router-dom";
import { ThemeProvider } from "@emotion/react";
import { CssBaseline } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { router } from "./router";
import theme from "./theme";
import { Provider } from "react-redux";
import { store } from "./store";

const App = () => {
  return (
    <>
      <Provider store={store}>
        <ThemeProvider theme={theme}>
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <CssBaseline />
            <RouterProvider router={router} />;
          </LocalizationProvider>
        </ThemeProvider>
      </Provider>
    </>
  );
};

export default App;
