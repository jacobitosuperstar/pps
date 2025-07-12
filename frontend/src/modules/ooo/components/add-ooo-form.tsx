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
import { useGetEmployeesOptionsInfiniteQuery } from "@/store/apis/employees.api";
import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2Icon } from "lucide-react";
import { useForm } from "react-hook-form";
import { Link, useNavigate } from "react-router-dom";
import { z } from "zod";
import { toast } from "sonner";
import {
  useCreateOOOMutation,
  useGetOOOTypesQuery,
} from "@/store/apis/ooo.api";
import { Textarea } from "@/components/ui/textarea";
import { SelectField } from "@/components/select-field";
import { useMemo } from "react";
import { ComboBoxInfinite } from "@/components/combobox-infinite";
import { useDebounceValue } from "usehooks-ts";

const oooFormSchema = z.object({
  employee: z.object(
    {
      id: z.number(),
      label: z.string(),
    },
    { message: "Este campo es requerido" }
  ),
  ooo_type: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  start_date: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  end_date: z.string().min(1, {
    message: "Este campo es requerido",
  }),
  description: z
    .string()
    .max(255, {
      message: "Este campo debe tener menos de 255 caracteres",
    }),
});

type OooFormType = z.infer<typeof oooFormSchema>;

export const AddOooForm = () => {
  const navigate = useNavigate();

  // states
  const [debouncedSearch, setDebouncedSearch] = useDebounceValue("", 500);

  // form
  const form = useForm<OooFormType>({
    resolver: zodResolver(oooFormSchema),
    defaultValues: {
      employee: undefined,
      ooo_type: undefined,
      start_date: "",
      end_date: "",
      description: "",
    },
  });

  // queries
  const { data: oooTypes = [] } = useGetOOOTypesQuery();

  const {
    data: employees,
    hasNextPage,
    isFetchingNextPage,
    fetchNextPage,
  } = useGetEmployeesOptionsInfiniteQuery({
    search: debouncedSearch,
  });

  const employeesOptions = useMemo(() => {
    if (employees?.pages) {
      return employees.pages.flatMap((page) => page.results);
    }
    return [];
  }, [employees]);

  // mutations
  const [createOOOMutation, { isLoading: isSubmitting }] =
    useCreateOOOMutation();

  // methods
  const onSubmit = (data: OooFormType) => {
    createOOOMutation({
      ...data,
      employee: data.employee?.id,
    })
      .unwrap()
      .then(() => {
        toast.success("Permiso creado exitosamente");
        navigate(PATHS.OOO.INDEX);
      })
      .catch(() => {
        toast.error("Error al crear el permiso");
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
          name="employee"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Empleado</FormLabel>
              <ComboBoxInfinite
                value={field.value}
                onChange={field.onChange}
                options={employeesOptions}
                onSearch={(query) => {
                  setDebouncedSearch(query);
                }}
                onLoadMore={() => {
                  fetchNextPage();
                }}
                hasNextPage={hasNextPage}
                isFetchingNextPage={isFetchingNextPage}
              />
              <FormMessage />
            </FormItem>
          )}
        />

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
