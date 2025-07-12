import { Button } from "@/components/ui/button";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { PATHS } from "@/constant/paths";
import { useLazyGetEmployeeByIdQuery } from "@/store/apis/employees.api";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { toast } from "sonner";
import {
  useGetOOOTypesQuery,
  useUpdateOOOMutation,
} from "@/store/apis/ooo.api";
import { Textarea } from "@/components/ui/textarea";
import { SelectField } from "@/components/select-field";
import { useEffect, useState } from "react";
import type { OOO } from "@/interfaces/ooo.interface";
import { format } from "date-fns";

const oooFormSchema = z.object({
  ooo_type: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  start_date: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  end_date: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  description: z.string().max(255, {
    message: "Este campo debe tener menos de 255 caracteres",
  }),
});

type OooFormType = z.infer<typeof oooFormSchema>;

interface Props {
  oooId: number;
  currentValues: OOO;
}

export const UpdateOooForm = ({ oooId, currentValues }: Props) => {
  const navigate = useNavigate();

  // states
  const [employee, setEmployee] = useState("");

  // form
  const form = useForm<OooFormType>({
    resolver: zodResolver(oooFormSchema),
    defaultValues: {
      ooo_type: currentValues.ooo_type,
      start_date: format(currentValues.start_date, "yyyy-MM-dd"),
      end_date: format(currentValues.end_date, "yyyy-MM-dd"),
      description: currentValues.description,
    },
  });

  // queries
  const { data: oooTypes = [] } = useGetOOOTypesQuery();

  const [getEmployeeById] = useLazyGetEmployeeByIdQuery();

  // mutations
  const [updateOOOMutation, { isLoading: isSubmitting }] =
    useUpdateOOOMutation();

  // methods
  const onSubmit = (data: OooFormType) => {
    updateOOOMutation({
      id: oooId,
      ...data,
    })
      .unwrap()
      .then(() => {
        toast.success("Permiso actualizado exitosamente");
        navigate(PATHS.OOO.INDEX);
      })
      .catch(() => {
        toast.error("Error al actualizar el permiso");
      });
  };

  // effects

  useEffect(() => {
    if (currentValues) {
      getEmployeeById(currentValues.employee.id)
        .unwrap()
        .then((res) => {
          setEmployee(`${res.names} ${res.last_names} - ${res.identification}`);
        })
        .catch(() => {
          toast.error("Error al obtener el empleado");
        });
    }
  }, [currentValues, getEmployeeById]);

  return (
    <Form {...form}>
      <form
        method="post"
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-6 min-h-screen"
      >
        <FormItem>
          <FormLabel>Empleado</FormLabel>
          <Input
            value={employee}
            onChange={() => {}}
            className="w-full"
            disabled
          />
        </FormItem>

        <FormField
          control={form.control}
          name="ooo_type"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Tipo de permiso</FormLabel>
              <SelectField
                value={field.value}
                onChange={field.onChange}
                options={oooTypes}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="start_date"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Fecha inicio</FormLabel>
              <Input
                type="date"
                placeholder="Ingrese la fecha de inicio del permiso"
                {...field}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="end_date"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Fecha fin</FormLabel>
              <Input
                type="date"
                placeholder="Ingrese la fecha de fin del permiso"
                {...field}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Descripción</FormLabel>
              <Textarea
                placeholder="Ingrese la descripción del permiso"
                {...field}
              />
              <FormMessage />
            </FormItem>
          )}
        />

        <div className="flex justify-end gap-4 pt-4">
          <Link to={PATHS.OOO.INDEX}>
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
