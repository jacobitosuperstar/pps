import { type ColumnDef } from '@tanstack/react-table'
import { type Machine } from '@/api/machines/queries/get-machines'
import { formatDateCell } from '@/lib/utils'
import { DataTableRowActions } from './data-table-row-actions'

export const machinesColumns: ColumnDef<Machine>[] = [
  {
    accessorKey: 'machine_code',
    header: 'Código',
    cell: ({ row }) => row.getValue('machine_code'),
  },
  {
    accessorKey: 'name',
    header: 'Nombre',
    cell: ({ row }) => row.getValue('name'),
  },
  {
    accessorKey: 'location',
    header: 'Ubicación',
    cell: ({ row }) => <div>{row.getValue('location')}</div>,
  },
  {
    accessorKey: 'model',
    header: 'Modelo',
    cell: ({ row }) => row.getValue('model'),
  },
  {
    accessorKey: 'created_at',
    header: 'Fecha de creación',
    cell: ({ row }) => formatDateCell(row.getValue('created_at')),
    enableColumnFilter: false,
  },
  {
    accessorKey: 'updated_at',
    header: 'Fecha de actualización',
    cell: ({ row }) => formatDateCell(row.getValue('updated_at')),
    enableColumnFilter: false,
  },
  {
    id: 'actions',
    cell: DataTableRowActions,
  },
]
