import {
  useCreateOooMutation,
  useGetAllOooQuery,
  useGetAllOooTypesQuery,
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
  IconButton,
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
import EditIcon from "@mui/icons-material/Edit";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import * as dayjs from "dayjs";
import { OOOModel } from "@/interfaces/employees.interface";

const schema = z
  .object({
    employeeIdentification: z
      .string()
      .min(1, "Este campo es requerido")
      .regex(/^\d+$/, "Debes agregar solo numeros"),
    oooType: z.string().min(1, "Este campo es requerido"),
    startDate: z.any().refine((value) => dayjs.isDayjs(value), {
      message: "Este campo es requerido",
    }),
    endDate: z.any().refine((value) => dayjs.isDayjs(value), {
      message: "Este campo es requerido",
    }),
    description: z.string().min(1, "Este campo es requerido"),
  })
  .required();

type FormData = z.infer<typeof schema>;

const OooPage = () => {
  // redux
  const oooQuery = useGetAllOooQuery();
  const oooTypesQuery = useGetAllOooTypesQuery();
  const [createOooMutation] = useCreateOooMutation();
  // states
  const [open, setOpen] = useState(false);
  const [currentOoo, setCurrentOoo] = useState<OOOModel | null>(null);
  // form control
  const formContext = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      employeeIdentification: "",
      oooType: "",
      startDate: "",
      endDate: "",
      description: "",
    },
  });
  // methods
  const onSubmit = async (formData: FormData) => {
    if (currentOoo) {
    } else {
      handleCreateOoo(formData);
    }
  };

  const handleCreateOoo = async (formData: FormData) => {
    try {
      const startDate = formData.startDate as dayjs.Dayjs;
      const endDate = formData.endDate as dayjs.Dayjs;

      const response = await createOooMutation({
        employee_identification: Number(formData.employeeIdentification),
        ooo_type: formData.oooType,
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        description: formData.description,
      }).unwrap();
      console.log(response);
      formContext.reset();
    } catch (error) {
      console.log(error);
    }
  };

  const handleButtonCreate = () => {
    setCurrentOoo(null);
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleButtonEdit = (ooo: OOOModel) => {
    setCurrentOoo(ooo);
    setOpen(true);
  };

  // effects
  useEffect(() => {
    if (currentOoo) {
      formContext.setValue(
        "employeeIdentification",
        currentOoo.employee.identification
      );
      formContext.setValue("oooType", currentOoo.ooo_type);
      formContext.setValue("startDate", dayjs(currentOoo.start_date));
      formContext.setValue("endDate", dayjs(currentOoo.end_date));
      formContext.setValue("description", currentOoo.description);
    } else {
      formContext.reset();
    }
  }, [currentOoo]);
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
        <Button
          color="primary"
          variant="contained"
          onClick={handleButtonCreate}
        >
          Crear permiso
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
              <TableCell align="right">Fecha inicio</TableCell>
              <TableCell align="right">Fecha Fin</TableCell>
              <TableCell align="right">Descripción</TableCell>
              <TableCell align="right"></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {oooQuery.data &&
              oooQuery.data.map((row) => (
                <TableRow
                  key={row.id}
                  sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                >
                  <TableCell component="th" scope="row">
                    {row.employee.identification}
                  </TableCell>
                  <TableCell align="right">{row.employee.names}</TableCell>
                  <TableCell align="right">{row.employee.last_names}</TableCell>
                  <TableCell align="right">{row.start_date}</TableCell>
                  <TableCell align="right">{row.end_date}</TableCell>
                  <TableCell align="right">{row.description}</TableCell>
                  <TableCell align="right">
                    <IconButton
                      onClick={() => handleButtonEdit(row)}
                      aria-label="editar"
                    >
                      <EditIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog maxWidth="sm" fullWidth open={open} onClose={handleClose}>
        <DialogTitle>
          {currentOoo ? "Editar permiso" : "Crear permiso"}
        </DialogTitle>
        <DialogContent>
          <FormContainer
            formContext={formContext}
            handleSubmit={formContext.handleSubmit(onSubmit)}
          >
            <Stack sx={{ paddingTop: "20px" }} spacing={2}>
              <TextFieldElement
                label="Identificación del empleado"
                name="employeeIdentification"
                id="employeeIdentification"
                required
              />

              <SelectElement
                label="Tipo de permiso"
                name="oooType"
                id="oooType"
                options={
                  !oooTypesQuery.data
                    ? []
                    : oooTypesQuery.data.map((x) => ({
                        id: x.id,
                        label: x.label,
                      }))
                }
              />

              <DatePickerElement
                label="Fecha inicio"
                name="startDate"
                inputProps={{ id: "startDate" }}
              />

              <DatePickerElement
                label="Fecha fin"
                name="endDate"
                inputProps={{ id: "endDate" }}
              />

              <TextFieldElement
                label="Descripción"
                name="description"
                id="description"
                required
                multiline
                rows={4}
              />

              <DialogActions>
                <LoadingButton
                  color="primary"
                  variant="outlined"
                  onClick={handleClose}
                >
                  Cerrar
                </LoadingButton>
                <LoadingButton
                  type="submit"
                  color="primary"
                  variant="contained"
                >
                  {currentOoo ? "Editar" : "Crear"}
                </LoadingButton>
              </DialogActions>
            </Stack>
          </FormContainer>
        </DialogContent>
      </Dialog>
    </>
  );
};

export default OooPage;
