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
import { Link, useSearchParams } from "react-router-dom";
import { PATHS } from "@/constant/paths";
import { Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import type { OOO } from "@/interfaces/ooo.interface";
import { useGetOOOTypesQuery } from "@/store/apis/ooo.api";
import { toLocalDateTime } from "@/helper/dates";

interface Props {
  data: OOO[];
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
  const { data: oooTypes = [] } = useGetOOOTypesQuery();

  const oooTypesDict = useMemo(() => {
    return oooTypes.reduce((acc, role) => {
      acc[role.value] = role.label;
      return acc;
    }, {} as Record<string, string>);
  }, [oooTypes]);

  const columns: ColumnDef<OOO>[] = [
    {
      accessorKey: "employee",
      header: "Empleado",
      cell: ({ row }) => <div>{row.getValue("employee")}</div>,
    },
    {
      accessorKey: "ooo_type",
      header: "Tipo",
      cell: ({ row }) => (
        <div>{oooTypesDict[row.getValue("ooo_type") as string]}</div>
      ),
    },
    {
      accessorKey: "description",
      header: "Descripción",
      cell: ({ row }) => <div>{row.getValue("description")}</div>,
    },
    {
      accessorKey: "start_date",
      header: "Fecha de inicio",
      cell: ({ row }) => (
        <div>{toLocalDateTime(row.getValue("start_date"), "dd/MM/yyyy")}</div>
      ),
    },
    {
      accessorKey: "end_date",
      header: "Fecha de fin",
      cell: ({ row }) => (
        <div>{toLocalDateTime(row.getValue("end_date"), "dd/MM/yyyy")}</div>
      ),
    },
    {
      id: "actions",
      cell: ({ row }) => {
        const ooo = row.original;

        return (
          <div className="flex items-center gap-2">
            <Link to={PATHS.OOO.EDIT.replace(":id", ooo.id.toString())}>
              <Button variant="default" size="icon" className="size-8">
                <Edit />
              </Button>
            </Link>
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
      <TableToolbar createUrl={PATHS.OOO.CREATE} table={table} />
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
