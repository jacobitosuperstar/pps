import { useQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { getCoreRowModel, useReactTable } from '@tanstack/react-table'
import getEmployeesQuery from '@/api/employees/queries/employees'
import { useTableUrlState } from '@/hooks/use-table-url-state'
import { ConfigDrawer } from '@/components/config-drawer'
import { DataTable } from '@/components/data-table/data-table'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ProfileDropdown } from '@/components/profile-dropdown'
import { ThemeSwitch } from '@/components/theme-switch'
import { employeesColumns } from './components/employees-columns'
import { EmployeeDialogs } from './components/employees-dialogs'
import { EmployeesPrimaryButtons } from './components/employees-primary-buttons'
import { EmployeeProvider } from './components/employees-provider'

const route = getRouteApi('/_authenticated/employees/')

export function Employees() {
  // router
  const search = route.useSearch()
  const navigate = route.useNavigate()

  // services
  const {
    data = { results: [], total_count: 0 },
    isLoading,
    isFetching,
  } = useQuery({
    queryKey: [
      'employees',
      search.identification,
      search.last_names,
      search.limit,
      search.names,
      search.offset,
      search.role,
      search.birthday,
    ],
    queryFn: () =>
      getEmployeesQuery({
        identification: search.identification,
        last_names: search.last_names,
        limit: search.limit,
        names: search.names,
        offset: search.offset,
        role: search.role,
        birthday: search.birthday,
      }),
  })

  // Table
  const {
    pagination,
    columnFilters,
    onPaginationChange,
    onColumnFiltersChange,
    pageSize,
  } = useTableUrlState({
    search,
    navigate,
    defaultPageSize: 10,
  })

  const table = useReactTable({
    data: data.results,
    columns: employeesColumns,
    state: {
      pagination,
      columnFilters,
    },
    manualPagination: true,
    pageCount: Math.ceil(data.total_count / pageSize),
    onPaginationChange,
    onColumnFiltersChange,
    getCoreRowModel: getCoreRowModel(),
  })

  return (
    <EmployeeProvider>
      <Header fixed>
        <div className='ms-auto flex items-center space-x-4'>
          <ThemeSwitch />
          <ConfigDrawer />
          <ProfileDropdown />
        </div>
      </Header>

      <Main>
        <div className='mb-2 flex flex-wrap items-center justify-between space-y-2'>
          <div>
            <h2 className='text-2xl font-bold tracking-tight'>
              Listado de Empleados
            </h2>
            <p className='text-muted-foreground'>
              Administra los empleados y sus roles aqui.
            </p>
          </div>

          <EmployeesPrimaryButtons />
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-y-0 lg:space-x-12'>
          <DataTable
            table={table}
            columns={employeesColumns}
            isLoading={isLoading}
            isFetching={isFetching}
          />
        </div>
      </Main>
      <EmployeeDialogs />
    </EmployeeProvider>
  )
}
