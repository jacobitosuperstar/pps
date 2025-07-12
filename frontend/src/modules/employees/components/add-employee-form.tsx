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
  useCreateEmployeeMutation,
  useGetRolesQuery,
} from "@/store/apis/employees.api";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { SelectField } from "@/components/select-field";
import { toast } from "sonner";

const clientFormSchema = z.object({
  identification: z
    .string()
    .min(6, { message: "La cédula debe tener al menos 6 dígitos" }) // puedes ajustar el mínimo
    .max(20, { message: "La cédula no debe tener más de 10 dígitos" }) // puedes ajustar el máximo
    .regex(/^\d+$/, { message: "La cédula solo debe contener números" }),
  names: z
    .string()
    .min(1, {
      message: "Este campo es requerido",
    })
    .max(100, {
      message: "Este campo debe tener menos de 100 caracteres",
    }),
  last_names: z
    .string()
    .min(1, {
      message: "Este campo es requerido",
    })
    .max(100, {
      message: "Este campo debe tener menos de 100 caracteres",
    }),
  role: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  birthday: z.string().min(1, {
    message: "Este campo es requerido",
  }),
});

type ClientFormType = z.infer<typeof clientFormSchema>;

export const AddEmployeeForm = () => {
  const navigate = useNavigate();

  // form
  const form = useForm<ClientFormType>({
    resolver: zodResolver(clientFormSchema),
    defaultValues: {
      identification: "",
      names: "",
      last_names: "",
      role: "",
      birthday: "",
    },
  });

  // queries
  const { data: roles = [] } = useGetRolesQuery();

  // mutations
  const [createEmployeeMutation, { isLoading: isSubmitting }] =
    useCreateEmployeeMutation();

  // methods
  const onSubmit = (data: ClientFormType) => {
    createEmployeeMutation({
      ...data,
    })
      .unwrap()
      .then(() => {
        toast.success("Cliente creado exitosamente");
        navigate(PATHS.EMPLOYEES.INDEX);
      })
      .catch(() => {
        toast.error("Error al crear el cliente");
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
          name="identification"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Cédula</FormLabel>
              <FormControl>
                <Input placeholder="Ingrese la cédula" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
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
