import { useQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { getCoreRowModel, useReactTable } from '@tanstack/react-table'
import getMachinesQuery from '@/api/machines/queries/get-machines'
import { useTableUrlState } from '@/hooks/use-table-url-state'
import { ConfigDrawer } from '@/components/config-drawer'
import { DataTable } from '@/components/data-table/data-table'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ProfileDropdown } from '@/components/profile-dropdown'
import { ThemeSwitch } from '@/components/theme-switch'
import { machinesColumns } from './components/machines-columns'
import { MachinesDialogs } from './components/machines-dialogs'
import { MachinesPrimaryButtons } from './components/machines-primary-buttons'
import { MachineProvider } from './components/machines-provider'

const route = getRouteApi('/_authenticated/machines/')

export function Machines() {
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
      'machines',
      search.machine_code,
      search.name,
      search.location,
      search.model,
      search.limit,
      search.offset,
    ],
    queryFn: () =>
      getMachinesQuery({
        machine_code: search.machine_code,
        name: search.name,
        location: search.location,
        model: search.model,
        limit: search.limit,
        offset: search.offset,
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
    columns: machinesColumns,
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
    <MachineProvider>
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
              Listado de Máquinas
            </h2>
            <p className='text-muted-foreground'>
              Administra las máquinas aqui.
            </p>
          </div>

          <MachinesPrimaryButtons />
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-y-0 lg:space-x-12'>
          <DataTable
            table={table}
            columns={machinesColumns}
            isLoading={isLoading}
            isFetching={isFetching}
          />
        </div>
      </Main>
      <MachinesDialogs />
    </MachineProvider>
  )
}
