import { useEffect, useState } from "react";
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ClientsTablePagination } from "./clients-table-pagination";
import { ClientsTableToolbar } from "./clients-table-toolbar";
import { columns } from "./columns";
import type { Employee } from "@/interfaces/employees.interface";
import { useSearchParams } from "react-router-dom";

interface Props {
  data: Employee[];
  isLoading: boolean;
}

export function EmployeesTable({ data, isLoading }: Props) {
  const [searchParams, setSearchParams] = useSearchParams();

  // Obtener valores iniciales desde la URL
  const initialGlobalFilter = searchParams.get("search") || "";
  const initialPageIndex = Number(searchParams.get("page") || "1") - 1;
  const initialPageSize = Number(searchParams.get("page_size") || "10");

  const [globalFilter, setGlobalFilter] = useState(initialGlobalFilter);
  const [pagination, setPagination] = useState({
    pageIndex: initialPageIndex,
    pageSize: initialPageSize,
  });

  // Sincronizar el globalFilter con la URL
  useEffect(() => {
    const params = new URLSearchParams(searchParams);

    // Global filter
    if (globalFilter) params.set("search", globalFilter);
    else params.delete("search");

    // Pagination
    params.set("page", String(pagination.pageIndex + 1));
    params.set("page_size", String(pagination.pageSize));

    setSearchParams(params);
  }, [globalFilter, pagination, setSearchParams, searchParams]);

  const table = useReactTable({
    data: data, // Aquí deberías usar los datos paginados del backend
    columns,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    onPaginationChange: setPagination,
    manualPagination: true,
    manualSorting: true,
    manualFiltering: true,
    state: {
      pagination,
      globalFilter,
    },
  });

  return (
    <div className="space-y-4">
      <ClientsTableToolbar table={table} />
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  Cargando...
                </TableCell>
              </TableRow>
            ) : table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && "selected"}
                  className="cursor-pointer hover:bg-muted/50"
                  //   onClick={() => router.push(`/clients/${row.original.id}`)}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No hay resultados.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <ClientsTablePagination table={table} />
    </div>
  );
}
