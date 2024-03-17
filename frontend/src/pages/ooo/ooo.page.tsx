import {
  useCreateOooMutation,
  useDeleteOooMutation,
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
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import * as dayjs from "dayjs";
import { CellTableMessage } from "@/components";
import { useSnackbar } from "notistack";
import { OOOModel } from "@/interfaces/employees.interface";
import { useConfirm } from "material-ui-confirm";
import { Delete } from "@mui/icons-material";

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
  const confirm = useConfirm();
  // redux
  const [deleteMutation, deleteContext] = useDeleteOooMutation();
  const employees = useGetEmployeesQuery();
  const oooQuery = useGetAllOooQuery();
  const oooTypesQuery = useGetAllOooTypesQuery();
  const [createOooMutation, createOooContext] = useCreateOooMutation();
  // states
  const [employeeList, setEmployeeList] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
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
  const handleButtonDelete = (row: OOOModel) => {
    confirm({
      title: "Eliminar permiso",
      description: "¿Seguro deseas eliminar este permiso?",
      confirmationText: "Confirmar",
      cancellationText: "Cancelar",
    })
      .then(async () => {
        const response = await deleteMutation(row.id).unwrap();
        console.log(response);
        enqueueSnackbar("Permiso eliminado con éxito", { variant: "success" });
      })
      .catch((error) => {
        console.log(error);
        enqueueSnackbar("Ocurrió un error", { variant: "error" });
      });
  };

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
            <TableCell align="left">
              {dayjs(new Date(row.start_date)).format("YYYY-MM-DD")}
            </TableCell>
            <TableCell align="left">
              {dayjs(new Date(row.end_date)).format("YYYY-MM-DD")}
            </TableCell>
            <TableCell align="left">{row.description}</TableCell>
            <TableCell align="left">
              <IconButton
                onClick={() => handleButtonDelete(row)}
                aria-label="eliminar"
              >
                <Delete />
              </IconButton>
            </TableCell>
          </TableRow>
        ))}
      </>
    );
  };

  const onSubmit = async (formData: FormData) => {
    try {
      const startDate = formData.startDate as dayjs.Dayjs;
      const endDate = formData.endDate as dayjs.Dayjs;

      const response = await createOooMutation({
        employee_identification: Number(formData.employee.id),
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
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  // effects
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

  useEffect(() => {
    setIsLoading(
      [deleteContext.isLoading, createOooContext.isLoading].some((x) => x)
    );
  }, [deleteContext, createOooContext]);
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
        <DialogTitle>Crear permiso</DialogTitle>
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
                loading={isLoading}
                required
              ></AutocompleteElement>

              <SelectElement
                disabled={isLoading}
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
                disabled={isLoading}
                label="Fecha inicio"
                name="startDate"
                inputProps={{ id: "startDate" }}
              />

              <DatePickerElement
                slotProps={{
                  popper: {
                    placement: "top-start",
                  },
                }}
                disabled={isLoading}
                label="Fecha fin"
                name="endDate"
                inputProps={{ id: "endDate" }}
              />

              <TextFieldElement
                disabled={isLoading}
                label="Descripción"
                name="description"
                id="description"
                required
                multiline
                rows={4}
              />

              <DialogActions>
                <LoadingButton
                  loading={isLoading}
                  color="primary"
                  variant="outlined"
                  onClick={handleClose}
                >
                  Cerrar
                </LoadingButton>
                <LoadingButton
                  loading={isLoading}
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

export default OooPage;
