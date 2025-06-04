import type { ColumnDef } from "@tanstack/react-table";
import { MoreHorizontal } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { Employee } from "@/interfaces/employees.interface";

export const columns: ColumnDef<Employee>[] = [
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
    cell: ({ row }) => <div>{row.getValue("role")}</div>,
  },
  {
    id: "actions",
    cell: ({ row }) => {
      const employee = row.original;

      return (
        <DropdownMenu>
          <DropdownMenuTrigger onClick={(e) => e.stopPropagation()} asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Abrir menú</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Acciones</DropdownMenuLabel>
            <DropdownMenuItem

            // onClick={() => router.push(`/clients/${client.id}`)}
            >
              Ver detalles
            </DropdownMenuItem>
            <DropdownMenuItem
            // onClick={() => router.push(`/clients/${client.id}/edit`)}
            >
              Editar
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              onClick={() => {
                // Show delete confirmation dialog
                if (
                  confirm(
                    `Estas seguro de eliminar ${employee.names} ${employee.last_names}?`
                  )
                ) {
                  console.log(`Deleting employee ${employee.identification}`);
                }
              }}
              className="text-destructive focus:text-destructive"
            >
              Borrar
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      );
    },
  },
];
