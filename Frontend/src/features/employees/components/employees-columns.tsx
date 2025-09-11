import { type ColumnDef } from '@tanstack/react-table'
import { type Employee } from '@/api/employees/queries/get-employees'
import { roles } from '../data/data'
import { DataTableRowActions } from './data-table-row-actions'

export const employeesColumns: ColumnDef<Employee>[] = [
  {
    accessorKey: 'identification',
    header: 'Identificación',
    cell: ({ row }) => row.getValue('identification'),
  },
  {
    accessorKey: 'names',
    header: 'Nombres',
    cell: ({ row }) => row.getValue('names'),
  },
  {
    accessorKey: 'last_names',
    header: 'Apellidos',
    cell: ({ row }) => row.getValue('last_names'),
  },
  {
    accessorKey: 'birthday',
    header: 'Cumpleaños',
    cell: ({ row }) => <div>{row.getValue('birthday')}</div>,
  },
  {
    accessorKey: 'role',
    header: 'Rol',
    cell: ({ row }) => {
      const { role } = row.original
      const userType = roles.find(({ value }) => value === role)

      if (!userType) {
        return null
      }

      return (
        <div className='flex items-center gap-x-2'>
          {userType.icon && (
            <userType.icon size={16} className='text-muted-foreground' />
          )}
          <span className='text-sm capitalize'>{userType.label}</span>
        </div>
      )
    },
    filterFn: (row, id, value) => {
      return value.includes(row.getValue(id))
    },
  },
  {
    id: 'actions',
    cell: DataTableRowActions,
  },
]
