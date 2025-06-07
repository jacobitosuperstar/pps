import { useEffect, useMemo, useState } from "react";
import {
  flexRender,
  getCoreRowModel,
  useReactTable,
  type ColumnDef,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { TablePagination } from "@/components/table-pagination";
import { TableToolbar } from "@/components/table-toolbar";
import type { Employee } from "@/interfaces/employees.interface";
import { Link, useSearchParams } from "react-router-dom";
import { PATHS } from "@/constant/paths";
import { Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useGetRolesQuery } from "@/store/apis/employees.api";
import { DeleteButton } from "./delete-button";

interface Props {
  data: Employee[];
  isLoading: boolean;
}

export function DataTable({ data, isLoading }: Props) {
  const [searchParams, setSearchParams] = useSearchParams();

  // states
  const initialGlobalFilter = searchParams.get("search") || "";
  const initialPageIndex = Number(searchParams.get("page") || "1") - 1;
  const initialPageSize = Number(searchParams.get("page_size") || "10");

  const [globalFilter, setGlobalFilter] = useState(initialGlobalFilter);
  const [pagination, setPagination] = useState({
    pageIndex: initialPageIndex,
    pageSize: initialPageSize,
  });

  // queries
  const { data: roles = [] } = useGetRolesQuery();
  const rolesDict = useMemo(() => {
    return roles.reduce((acc, role) => {
      acc[role.value] = role.label;
      return acc;
    }, {} as Record<string, string>);
  }, [roles]);

  const columns: ColumnDef<Employee>[] = [
    {
      accessorKey: "identification",
      header: "Identificación",
      cell: ({ row }) => <div>{row.getValue("identification")}</div>,
    },
    {
      accessorKey: "names",
      header: "Nombre",
      cell: ({ row }) => <div>{row.getValue("names")}</div>,
    },
    {
      accessorKey: "last_names",
      header: "Apellido",
      cell: ({ row }) => <div>{row.getValue("last_names")}</div>,
    },
    {
      accessorKey: "role",
      header: "Rol",
      cell: ({ row }) => <div>{rolesDict[row.getValue("role") as string]}</div>,
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const employee = row.original;

        return (
          <div className="flex items-center gap-2">
            <Link
              to={PATHS.EMPLOYEES.EDIT.replace(":id", employee.id.toString())}
            >
              <Button variant="default" size="icon" className="size-8">
                <Edit />
              </Button>
            </Link>
            <DeleteButton employeeId={employee.id} />
          </div>
        );
      },
    },
  ];

  const table = useReactTable({
    data: data,
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

  // effects
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

  return (
    <div className="space-y-4">
      <TableToolbar table={table} createUrl={PATHS.EMPLOYEES.CREATE} />
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
                  //   onClick={() => router.push(`//${row.original.id}`)}
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
      <TablePagination table={table} />
    </div>
  );
}
