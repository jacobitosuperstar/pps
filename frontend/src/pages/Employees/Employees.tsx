import { Roles } from "@/interfaces/employees.interface";
import {
  useCreateEmployeeMutation,
  useGetEmployeesQuery,
  useGetRolesQuery,
} from "@/store/apis";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoadingButton } from "@mui/lab";
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  MenuItem,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod";

const schema = z
  .object({
    identification: z.string().min(1, "Este campo es requerido"),
    names: z.string().min(1, "Este campo es requerido"),
    lastNames: z.string().min(1, "Este campo es requerido"),
    birthday: z.string().min(1, "Este campo es requerido"),
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
  console.log(employees, 'mirar aqui');
  console.log(roles.data);

  // states
  const [open, setOpen] = useState(false);

  // form control
  // form control
  const { control, handleSubmit, reset } = useForm<FormData>({
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
      const response = await createEmployeeMutation({
        birthday: formData.birthday,
        identification: formData.identification,
        last_names: formData.lastNames,
        names: formData.names,
        role: formData.role,
      }).unwrap();
      console.log(response);

      reset();
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

      <Dialog maxWidth="sm" fullWidth open={open} onClose={handleClose}>
        <DialogTitle>Crear empleado</DialogTitle>
        <DialogContent>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit(onSubmit)}
            sx={{ mt: 1 }}
          >
            <Controller
              name="identification"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={createEmployeeContext.isLoading}
                  margin="normal"
                  required
                  fullWidth
                  id="identification"
                  label="Identificación"
                  type="text"
                  autoFocus
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                />
              )}
            />

            <Controller
              name="names"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={createEmployeeContext.isLoading}
                  margin="normal"
                  required
                  fullWidth
                  id="names"
                  label="Nombre"
                  type="text"
                  autoFocus
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                />
              )}
            />

            <Controller
              name="lastNames"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={createEmployeeContext.isLoading}
                  margin="normal"
                  required
                  fullWidth
                  id="lastNames"
                  label="Apellido"
                  type="text"
                  autoFocus
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                />
              )}
            />

            <Controller
              name="birthday"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={createEmployeeContext.isLoading}
                  margin="normal"
                  required
                  fullWidth
                  id="birthday"
                  label="Fecha de nacimiento"
                  type="date"
                  autoFocus
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                />
              )}
            />

            <Controller
              name="role"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={createEmployeeContext.isLoading}
                  margin="normal"
                  select
                  required
                  fullWidth
                  id="role"
                  label="Rol"
                  type="date"
                  autoFocus
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                >
                  {roles.data &&
                    Object.keys(roles.data).map((key) => (
                      <MenuItem key={key} value={key}>
                        {String(roles.data![key as keyof Roles]).toUpperCase()}
                      </MenuItem>
                    ))}
                </TextField>
              )}
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
          </Box>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default EmployeesPage;
