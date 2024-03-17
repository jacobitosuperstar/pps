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
import WidgetsIcon from "@mui/icons-material/Widgets";
import ErrorOutlineIcon from "@mui/icons-material/ErrorOutline";
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
import { useSnackbar } from "notistack";
import { CellTableMessage } from "@/components";

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
  // notifications
  const { enqueueSnackbar } = useSnackbar();
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
  const renderTableBody = () => {
    if (employees.error) {
      return (
        <CellTableMessage
          message="Ocurrió un error al obtener la información"
          icon={<ErrorOutlineIcon />}
          colSpan={4}
        />
      );
    }

    if (!employees.data?.length) {
      return (
        <CellTableMessage
          message="No hay datos para mostrar"
          icon={<WidgetsIcon />}
          colSpan={4}
        />
      );
    }

    return (
      <>
        {employees.data.map((row) => (
          <TableRow
            key={row.identification}
            sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
          >
            <TableCell component="th" scope="row">
              {row.identification}
            </TableCell>
            <TableCell align="left">{row.names}</TableCell>
            <TableCell align="left">{row.last_names}</TableCell>
            <TableCell align="left">
              {!roles.data
                ? ""
                : roles.data
                    .find((x) => x.id === row.role)
                    ?.name?.toUpperCase()}
            </TableCell>
          </TableRow>
        ))}
      </>
    );
  };

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
      enqueueSnackbar("Empleado creado con éxito", { variant: "success" });
      formContext.reset();
    } catch (error) {
      console.log(error);
      enqueueSnackbar("Ocurrió un error", { variant: "error" });
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
              <TableCell align="left">Identificación</TableCell>
              <TableCell align="left">Nombre</TableCell>
              <TableCell align="left">Apellido</TableCell>
              <TableCell align="left">Rol</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>{renderTableBody()}</TableBody>
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
