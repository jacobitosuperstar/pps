import {
  useCreateEmployeeMutation,
  useGetEmployeesQuery,
  useGetRolesQuery,
} from "@/store/apis";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoadingButton } from "@mui/lab";
import {
  FormContainer,
  TextFieldElement,
  SelectElement,
  DatePickerElement,
} from "react-hook-form-mui";
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import * as dayjs from "dayjs";

const schema = z
  .object({
    identification: z
      .string()
      .min(1, "Este campo es requerido")
      .regex(/^\d+$/, "Debes agregar solo numeros"),
    names: z
      .string()
      .min(1, "Este campo es requerido")
      .regex(/^[a-zA-Z\s]+$/, "Debes agregar solo letras y espacios"),
    lastNames: z
      .string()
      .min(1, "Este campo es requerido")
      .regex(/^[a-zA-Z\s]+$/, "Debes agregar solo letras y espacios"),
    birthday: z.any().refine((value) => dayjs.isDayjs(value), {
      message: "Este campo es requerido",
    }),
    role: z.string().min(1, "Este campo es requerido"),
  })
  .required();

type FormData = z.infer<typeof schema>;

const EmployeesPage = () => {
  // redux
  const employees = useGetEmployeesQuery();
  const roles = useGetRolesQuery();
  const [createEmployeeMutation, createEmployeeContext] =
    useCreateEmployeeMutation();

  // states
  const [open, setOpen] = useState(false);

  // form control
  const formContext = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      identification: "",
      names: "",
      lastNames: "",
      birthday: "",
      role: "",
    },
  });

  // methods
  const onSubmit = async (formData: FormData) => {
    try {
      const date = formData.birthday as dayjs.Dayjs;
      const response = await createEmployeeMutation({
        birthday: date.format("YYYY-MM-DD"),
        identification: formData.identification,
        last_names: formData.lastNames,
        names: formData.names,
        role: formData.role,
      }).unwrap();
      console.log(response);
      formContext.reset();
    } catch (error) {
      console.log(error);
    }
  };

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
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
          Empleados
        </Typography>
        <Button color="primary" variant="contained" onClick={handleClickOpen}>
          Crear empleado
        </Button>
      </Box>
      <Divider></Divider>

      <TableContainer sx={{ marginTop: "30px" }} component={Paper}>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell align="right">Identificación</TableCell>
              <TableCell align="right">Nombre</TableCell>
              <TableCell align="right">Apellido</TableCell>
              <TableCell align="right">Rol</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {employees.data &&
              employees.data.map((row) => (
                <TableRow
                  key={row.identification}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.identification}
                  </TableCell>
                  <TableCell align="right">{row.names}</TableCell>
                  <TableCell align="right">{row.last_names}</TableCell>
                  <TableCell align="right">
                    {!roles.data
                      ? ""
                      : roles.data
                          .find((x) => x.id === row.role)
                          ?.name?.toUpperCase()}
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog maxWidth="sm" fullWidth open={open} onClose={handleClose}>
        <DialogTitle>Crear empleado</DialogTitle>
        <DialogContent>
          <FormContainer
            formContext={formContext}
            handleSubmit={formContext.handleSubmit(onSubmit)}
          >
            <Stack sx={{ paddingTop: "20px" }} spacing={2}>
              <TextFieldElement
                label="Identificación"
                name="identification"
                id="identification"
                required
              />

              <TextFieldElement
                label="Nombre"
                name="names"
                id="names"
                required
              />

              <TextFieldElement
                label="Apellido"
                name="lastNames"
                id="lastNames"
                required
              />

              <DatePickerElement
                label="Fecha de nacimiento"
                name="birthday"
                inputProps={{ id: "birthday" }}
              />

              <SelectElement
                label="Roles"
                name="role"
                id="role"
                options={
                  !roles.data
                    ? []
                    : roles.data.map((x) => ({ id: x.id, label: x.name }))
                }
              />

              <DialogActions>
                <LoadingButton
                  loading={createEmployeeContext.isLoading}
                  color="primary"
                  variant="outlined"
                  onClick={handleClose}
                >
                  Cerrar
                </LoadingButton>
                <LoadingButton
                  loading={createEmployeeContext.isLoading}
                  type="submit"
                  color="primary"
                  variant="contained"
                >
                  Crear
                </LoadingButton>
              </DialogActions>
            </Stack>
          </FormContainer>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default EmployeesPage;
