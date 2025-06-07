import { useGetEmployeesQuery } from "@/store/apis/employees.api";
import { DataTable } from "../components/data-table";
import { useSearchParams } from "react-router-dom";

export default function EmployeesPage() {
  const [searchParams] = useSearchParams();

  // Obtener valores iniciales desde la URL
  const initialGlobalFilter = searchParams.get("search") || "";
  const initialPageIndex = Number(searchParams.get("page") || "1") - 1;
  const initialPageSize = Number(searchParams.get("page_size") || "10");

  const { data, isLoading } = useGetEmployeesQuery({
    search: initialGlobalFilter,
    page: initialPageIndex + 1,
    page_size: initialPageSize,
  });

  const employees = data?.results || [];

  return (
    <div className="flex flex-col gap-6 p-6 md:p-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight mb-2">Empleados</h2>
        <p className="text-muted-foreground">
          Gestiona los empleados de tu empresa.
        </p>
      </div>
      <DataTable data={employees} isLoading={isLoading} />
    </div>
  );
}
