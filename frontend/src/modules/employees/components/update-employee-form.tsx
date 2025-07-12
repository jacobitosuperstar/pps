import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { PATHS } from "@/constant/paths";
import {
  useGetRolesQuery,
  useUpdateEmployeeMutation,
} from "@/store/apis/employees.api";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { SelectField } from "@/components/select-field";
import { toast } from "sonner";
import type { Employee } from "@/interfaces/employees.interface";
import { format } from "date-fns";

const clientFormSchema = z.object({
  names: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  last_names: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  role: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  birthday: z.string().min(1, {
    message: "Este campo es requerido",
  }),
});

type ClientFormType = z.infer<typeof clientFormSchema>;

interface Props {
  employeeId: number;
  currentValues: Employee;
}

export const UpdateEmployeeForm = ({ employeeId, currentValues }: Props) => {
  const navigate = useNavigate();

  // form
  const form = useForm<ClientFormType>({
    resolver: zodResolver(clientFormSchema),
    defaultValues: {
      names: currentValues.names,
      last_names: currentValues.last_names,
      role: currentValues.role,
      birthday: currentValues.birthday
        ? format(currentValues.birthday, "yyyy-MM-dd")
        : "",
    },
  });

  // queries
  const { data: roles = [] } = useGetRolesQuery();

  // mutations
  const [updateEmployeeMutation, { isLoading: isSubmitting }] =
    useUpdateEmployeeMutation();

  // methods
  const onSubmit = (data: ClientFormType) => {
    updateEmployeeMutation({
      id: employeeId,
      ...data,
    })
      .unwrap()
      .then(() => {
        toast.success("Cliente actualizado exitosamente");
        navigate(PATHS.EMPLOYEES.INDEX);
      })
      .catch(() => {
        toast.error("Error al actualizar el cliente");
      });
  };

  return (
    <Form {...form}>
      <form
        method="post"
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-6 min-h-screen"
      >
        <FormField
          control={form.control}
          name="names"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Nombre</FormLabel>
              <FormControl>
                <Input placeholder="Ingrese el nombre" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="last_names"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Apellido</FormLabel>
              <FormControl>
                <Input placeholder="Ingrese el apellido" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="role"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Rol</FormLabel>
              <SelectField
                value={field.value}
                onChange={field.onChange}
                options={roles}
              />
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="birthday"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Fecha de nacimiento</FormLabel>
              <Input
                type="date"
                placeholder="Ingrese la fecha de nacimiento"
                {...field}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end gap-4 pt-4">
          <Link to={PATHS.EMPLOYEES.INDEX}>
            <Button type="button" variant="outline" disabled={isSubmitting}>
              Cancelar
            </Button>
          </Link>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting && <Loader2Icon className="animate-spin" />}
            Guardar
          </Button>
        </div>
      </form>
    </Form>
  );
};
