import { type ColumnDef } from '@tanstack/react-table'
import { type Client } from '@/api/clients/queries/get-clients'
import { formatDateCell } from '@/lib/utils'
import { DataTableRowActions } from './data-table-row-actions'

export const clientsColumns: ColumnDef<Client>[] = [
  {
    accessorKey: 'client_name',
    header: 'Nombre',
    cell: ({ row }) => row.getValue('client_name'),
  },
  {
    accessorKey: 'client_email',
    header: 'Email',
    cell: ({ row }) => row.getValue('client_email'),
  },
  {
    accessorKey: 'client_phone_code',
    header: 'Código de país',
    cell: ({ row }) => <div>{row.getValue('client_phone_code')}</div>,
  },
  {
    accessorKey: 'client_phone_number',
    header: 'Número de teléfono',
    cell: ({ row }) => row.getValue('client_phone_number'),
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
