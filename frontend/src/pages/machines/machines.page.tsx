import {
  useGetExistingMachinesTypesQuery,
  useGetMachinesTypesQuery,
} from "@/store/apis/machines.api";
import { Box, Button, Divider, Typography } from "@mui/material";

const MachinesPage = () => {
  // redux
  const machinesTypes = useGetMachinesTypesQuery();
  const existingMachinesTypes = useGetExistingMachinesTypesQuery();

  console.log(machinesTypes, existingMachinesTypes);

  // methods
  const handleClickOpen = () => {};
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
          Tipos de maquinas
        </Typography>
        <Button color="primary" variant="contained" onClick={handleClickOpen}>
          Crear tipo de maquina
        </Button>
      </Box>
      <Divider></Divider>
    </>
  );
};

export default MachinesPage;
