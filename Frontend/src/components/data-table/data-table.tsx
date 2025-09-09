import { useState } from 'react'
import {
  type ColumnDef,
  flexRender,
  type Table as TTable,
} from '@tanstack/react-table'
import { cn } from '@/lib/utils'
import { Input } from '@/components/ui/input'
import { Popover, PopoverAnchor, PopoverContent } from '@/components/ui/popover'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import {
  DataTableColumnHeader,
  DataTablePagination,
} from '@/components/data-table'
import { Button } from '../ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select'
import { Spinner } from '../ui/spinner'

declare module '@tanstack/react-table' {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  interface ColumnMeta<TData, TValue> {
    className: string
  }
}

type DataTableProps = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  table: TTable<any>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  columns: ColumnDef<any>[]
  isLoading?: boolean
  isFetching?: boolean
}

export const DataTable = ({
  table,
  columns,
  isLoading,
  isFetching,
}: DataTableProps) => {
  const [openPopover, setOpenPopover] = useState(false)
  const [activeColumn, setActiveColumn] = useState<string>('')
  const [filterValue, setFilterValue] = useState<string>('')

  const handleHeaderClick = (columnId: string) => {
    if (activeColumn === columnId) {
      setOpenPopover(!openPopover) // toggle si vuelves a hacer click en la misma columna
    } else {
      setActiveColumn(columnId)
      setOpenPopover(true)
    }
  }

  return (
    <div className='space-y-4 max-sm:has-[div[role="toolbar"]]:mb-16'>
      <Popover open={openPopover} onOpenChange={setOpenPopover}>
        <div className='overflow-hidden rounded-md border'>
          <Table>
            <PopoverAnchor asChild>
              <TableHeader>
                {table.getHeaderGroups().map((headerGroup) => (
                  <TableRow key={headerGroup.id} className='group/row'>
                    {headerGroup.headers.map((header) => {
                      return (
                        <TableHead
                          key={header.id}
                          colSpan={header.colSpan}
                          className={cn(
                            'group',
                            header.column.columnDef.meta?.className ?? ''
                          )}
                        >
                          {header.isPlaceholder ? null : (
                            <DataTableColumnHeader
                              onClick={() =>
                                handleHeaderClick(header.column.id)
                              }
                              column={header.column}
                            >
                              {flexRender(
                                header.column.columnDef.header,
                                header.getContext()
                              )}
                            </DataTableColumnHeader>
                          )}
                        </TableHead>
                      )
                    })}
                  </TableRow>
                ))}
              </TableHeader>
            </PopoverAnchor>
            <TableBody>
              {isLoading ? (
                // Loading inicial: spinner ocupa toda la tabla
                <TableRow>
                  <TableCell
                    colSpan={columns.length}
                    className='h-24 text-center'
                  >
                    <Spinner />
                  </TableCell>
                </TableRow>
              ) : table.getRowModel().rows?.length ? (
                <>
                  {/* Spinner de refresco: se muestra arriba pero no bloquea filas */}
                  {isFetching && (
                    <TableRow>
                      <TableCell
                        colSpan={columns.length}
                        className='h-12 text-center'
                      >
                        <Spinner size='small' />
                      </TableCell>
                    </TableRow>
                  )}

                  {table.getRowModel().rows.map((row) => (
                    <TableRow
                      key={row.id}
                      data-state={row.getIsSelected() && 'selected'}
                      className='group/row'
                    >
                      {row.getVisibleCells().map((cell) => (
                        <TableCell
                          key={cell.id}
                          className={cn(
                            cell.column.columnDef.meta?.className ?? ''
                          )}
                        >
                          {flexRender(
                            cell.column.columnDef.cell,
                            cell.getContext()
                          )}
                        </TableCell>
                      ))}
                    </TableRow>
                  ))}
                </>
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={columns.length}
                    className='h-24 text-center'
                  >
                    No hay resultados.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
        <DataTablePagination table={table} />

        {/* PopOver with filter */}

        <PopoverContent className='w-96' side='bottom' align='end'>
          <div className='flex flex-col gap-2'>
            <span className='text-sm font-medium'>Filtrar</span>
            <div className='mb-4 flex gap-2'>
              <Select value={activeColumn} onValueChange={setActiveColumn}>
                <SelectTrigger>
                  <SelectValue
                    className='w-40'
                    placeholder='Seleccionar columna'
                  />
                </SelectTrigger>
                <SelectContent>
                  {table
                    .getAllColumns()
                    .filter((col) => col.getCanFilter())
                    .map((col) => (
                      <SelectItem
                        key={col.id}
                        value={col.id}
                        onClick={() => setActiveColumn(col.id)}
                      >
                        {col.columnDef.header as string}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
              <Input
                value={filterValue}
                onChange={(e) => setFilterValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    e.stopPropagation()

                    table.getAllColumns().forEach((col) => {
                      if (col.getCanFilter()) col.setFilterValue('')
                    })

                    const col = table.getColumn(activeColumn)

                    col?.setFilterValue(filterValue)

                    setOpenPopover(false)
                  }
                }}
                placeholder='Buscar...'
              />
            </div>
            <div className='flex justify-end gap-2'>
              <Button
                onClick={() => {
                  table.getAllColumns().forEach((col) => {
                    if (col.getCanFilter()) col.setFilterValue('')
                  })

                  const col = table.getColumn(activeColumn)

                  col?.setFilterValue(filterValue)

                  setOpenPopover(false)
                }}
              >
                Aplicar
              </Button>
              <Button
                onClick={() => {
                  table.getAllColumns().forEach((col) => {
                    if (col.getCanFilter()) col.setFilterValue('')
                  })
                  setFilterValue('')
                  setActiveColumn('')
                  setOpenPopover(false)
                }}
                variant='outline'
              >
                Limpiar
              </Button>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </div>
  )
}
