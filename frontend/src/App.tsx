import { RouterProvider } from "react-router-dom";
import { ThemeProvider } from "@emotion/react";
import { CssBaseline } from "@mui/material";
import { router } from "./router";
import theme from "./theme";
import { Provider } from "react-redux";
import { store } from "./store";

const App = () => {
  return (
    <>
      <Provider store={store}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <RouterProvider router={router} />;
        </ThemeProvider>
      </Provider>
    </>
  );
};

export default App;
