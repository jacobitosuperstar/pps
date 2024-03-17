import {
  useCreateOooMutation,
  useGetAllOooQuery,
  useGetAllOooTypesQuery,
  useGetEmployeesQuery,
} from "@/store/apis";
import { zodResolver } from "@hookform/resolvers/zod";
import { LoadingButton } from "@mui/lab";
import {
  FormContainer,
  TextFieldElement,
  SelectElement,
  DatePickerElement,
  AutocompleteElement,
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
import { CellTableMessage } from "@/components";
import { useSnackbar } from "notistack";

const schema = z
  .object({
    employee: z.object({
      id: z.string().min(1, "Este campo es requerido"),
      label: z.string().min(1, "Este campo es requerido"),
    }),
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
  // notifications
  const { enqueueSnackbar } = useSnackbar();
  // redux
  const employees = useGetEmployeesQuery();
  const oooQuery = useGetAllOooQuery();
  const oooTypesQuery = useGetAllOooTypesQuery();
  const [createOooMutation] = useCreateOooMutation();
  // states
  const [employeeList, setEmployeeList] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [currentOoo, setCurrentOoo] = useState<OOOModel | null>(null);
  // form control
  const formContext = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      employee: {
        id: "",
        label: "",
      },
      oooType: "",
      startDate: "",
      endDate: "",
      description: "",
    },
  });
  // methods
  const renderTableBody = () => {
    if (oooQuery.error) {
      return (
        <CellTableMessage
          message="Ocurrió un error al obtener la información"
          icon={<ErrorOutlineIcon />}
          colSpan={7}
        />
      );
    }

    if (!oooQuery.data?.length) {
      return (
        <CellTableMessage
          message="No hay datos para mostrar"
          icon={<WidgetsIcon />}
          colSpan={7}
        />
      );
    }

    return (
      <>
        {oooQuery.data.map((row) => (
          <TableRow
            key={row.id}
            sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
          >
            <TableCell component="th" scope="row">
              {row.employee.identification}
            </TableCell>
            <TableCell align="left">{row.employee.names}</TableCell>
            <TableCell align="left">{row.employee.last_names}</TableCell>
            <TableCell align="left">{row.start_date}</TableCell>
            <TableCell align="left">{row.end_date}</TableCell>
            <TableCell align="left">{row.description}</TableCell>
            <TableCell align="left">
              <IconButton
                onClick={() => handleButtonEdit(row)}
                aria-label="editar"
              >
                <EditIcon />
              </IconButton>
            </TableCell>
          </TableRow>
        ))}
      </>
    );
  };

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
      console.log({
        employee_identification: Number(formData.employee.id),
        ooo_type: formData.oooType,
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        description: formData.description,
      });
      return;
      const response = await createOooMutation({
        employee_identification: Number(formData.employee),
        ooo_type: formData.oooType,
        start_date: startDate.toISOString(),
        end_date: endDate.toISOString(),
        description: formData.description,
      }).unwrap();
      console.log(response);
      enqueueSnackbar("Permiso creado con éxito", { variant: "success" });
      formContext.reset();
    } catch (error) {
      console.log(error);
      enqueueSnackbar("Ocurrió un error", { variant: "error" });
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
      formContext.setValue("employee", {
        id: currentOoo.employee.identification,
        label: currentOoo.employee.names
          .concat(" ")
          .concat(currentOoo.employee.last_names),
      });
      formContext.setValue("oooType", currentOoo.ooo_type);
      formContext.setValue("startDate", dayjs(currentOoo.start_date));
      formContext.setValue("endDate", dayjs(currentOoo.end_date));
      formContext.setValue("description", currentOoo.description);
    } else {
      formContext.reset();
    }
  }, [currentOoo]);

  useEffect(() => {
    if (employees.data) {
      setEmployeeList(
        employees.data.map((x) => ({
          id: x.identification,
          label: x.names.concat(" ").concat(x.last_names),
        }))
      );
    } else {
      setEmployeeList([]);
    }
  }, [employees]);
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
              <TableCell align="left">Identificación</TableCell>
              <TableCell align="left">Nombre</TableCell>
              <TableCell align="left">Apellido</TableCell>
              <TableCell align="left">Fecha inicio</TableCell>
              <TableCell align="left">Fecha Fin</TableCell>
              <TableCell align="left">Descripción</TableCell>
              <TableCell align="left"></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>{renderTableBody()}</TableBody>
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
              <AutocompleteElement
                autocompleteProps={{
                  isOptionEqualToValue: (option, value) =>
                    option.id === value.id,
                }}
                options={employeeList}
                label="Identificación del empleado"
                name="employee"
                loading={employees.isLoading}
                required
              ></AutocompleteElement>

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
