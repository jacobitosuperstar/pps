import { Box, Divider, Typography } from "@mui/material";

const HomePage = () => {
  return (
    <>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
      </Box>
      <Divider></Divider>
    </>
  );
};

export default HomePage;
