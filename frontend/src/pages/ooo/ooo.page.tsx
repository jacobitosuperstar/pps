import { useGetAllOooQuery } from "@/store/apis";
import { Box, Button, Divider, Typography } from "@mui/material";

const OooPage = () => {
  const oooQuery = useGetAllOooQuery();
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
          Permisos
        </Typography>
        <Button color="primary" variant="contained">
          Crear empleado
        </Button>
      </Box>
      <Divider></Divider>
    </>
  );
};

export default OooPage;
