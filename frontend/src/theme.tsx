import { createTheme } from "@mui/material/styles";
import { esES } from "@mui/x-date-pickers/locales";

// A custom theme for this app
const theme = createTheme(
  {
    palette: {
      primary: {
        main: "#00695f",
      },
      secondary: {
        main: "#FF5722",
      },
    },
  },
  esES
);

export default theme;
