import { DataTable } from "../components/data-table";
import { useSearchParams } from "react-router-dom";
import { useGetAllOOOQuery } from "@/store/apis/ooo.api";

export default function OooListPage() {
  const [searchParams] = useSearchParams();

  // Obtener valores iniciales desde la URL
  const initialGlobalFilter = searchParams.get("search") || "";
  const initialPageIndex = Number(searchParams.get("page") || "1") - 1;
  const initialPageSize = Number(searchParams.get("page_size") || "10");

  const { data, isLoading } = useGetAllOOOQuery({
    search: initialGlobalFilter,
    page: initialPageIndex + 1,
    page_size: initialPageSize,
  });

  const ooo = data?.results || [];

  return (
    <div className="flex flex-col gap-6 p-6 md:p-8">
      <div>
        <h2 className="text-3xl font-bold tracking-tight mb-2">Permisos</h2>
        <p className="text-muted-foreground">
          Gestiona los permisos de tus empleados.
        </p>
      </div>
      <DataTable data={ooo} isLoading={isLoading} />
    </div>
  );
}
