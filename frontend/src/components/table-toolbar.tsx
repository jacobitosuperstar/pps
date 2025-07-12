import type { Table } from "@tanstack/react-table";
import { Plus, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useDebounceValue } from "usehooks-ts";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link } from "react-router-dom";

interface TableToolbarProps<TData> {
  table: Table<TData>;
  createUrl?: string;
}

export function TableToolbar<TData>({
  table,
  createUrl,
}: TableToolbarProps<TData>) {
  const isFiltered =
    table.getState().columnFilters.length > 0 ||
    table.getState().globalFilter !== "";

  const [inputValue, setInputValue] = useState(table.getState().globalFilter);
  const [debouncedFilter] = useDebounceValue(inputValue, 500);

  useEffect(() => {
    table.setGlobalFilter(debouncedFilter);
  }, [debouncedFilter, table]);

  return (
    <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-1 items-center space-x-2">
        <Input
          placeholder="Buscar empleados..."
          value={inputValue}
          onChange={(event) => setInputValue(event.target.value)}
          className="h-10 w-full sm:w-[300px]"
        />
        {isFiltered && (
          <Button
            variant="ghost"
            onClick={() => {
              table.resetColumnFilters();
              table.setGlobalFilter("");
              setInputValue("");
            }}
            className="h-10 px-2 lg:px-3"
          >
            Limpiar
            <X className="ml-2 h-4 w-4" />
          </Button>
        )}
      </div>
      <div className="flex flex-wrap items-center gap-2">
        {createUrl && (
          <Link to={createUrl}>
            <Button variant="outline" size="sm" className="ml-auto h-10">
              Nuevo <Plus />
            </Button>
          </Link>
        )}
      </div>
    </div>
  );
}
