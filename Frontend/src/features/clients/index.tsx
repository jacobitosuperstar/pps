import { useQuery } from '@tanstack/react-query'
import { getRouteApi } from '@tanstack/react-router'
import { getCoreRowModel, useReactTable } from '@tanstack/react-table'
import getClientsQuery from '@/api/clients/queries/get-clients'
import { useTableUrlState } from '@/hooks/use-table-url-state'
import { ConfigDrawer } from '@/components/config-drawer'
import { DataTable } from '@/components/data-table/data-table'
import { Header } from '@/components/layout/header'
import { Main } from '@/components/layout/main'
import { ProfileDropdown } from '@/components/profile-dropdown'
import { ThemeSwitch } from '@/components/theme-switch'
import { clientsColumns } from './components/clients-columns'
import { ClientDialogs } from './components/clients-dialogs'
import { ClientsPrimaryButtons } from './components/clients-primary-buttons'
import { ClientProvider } from './components/clients-provider'

const route = getRouteApi('/_authenticated/clients/')

export function Clients() {
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
      'clients',
      search.client_name,
      search.client_email,
      search.client_phone_number,
      search.limit,
      search.offset,
    ],
    queryFn: () =>
      getClientsQuery({
        client_name: search.client_name,
        client_email: search.client_email,
        client_phone_number: search.client_phone_number,
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
    columns: clientsColumns,
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
    <ClientProvider>
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
              Listado de Clientes
            </h2>
            <p className='text-muted-foreground'>
              Administra los clientes aqui.
            </p>
          </div>

          <ClientsPrimaryButtons />
        </div>
        <div className='-mx-4 flex-1 overflow-auto px-4 py-1 lg:flex-row lg:space-y-0 lg:space-x-12'>
          <DataTable
            table={table}
            columns={clientsColumns}
            isLoading={isLoading}
            isFetching={isFetching}
          />
        </div>
      </Main>
      <ClientDialogs />
    </ClientProvider>
  )
}
