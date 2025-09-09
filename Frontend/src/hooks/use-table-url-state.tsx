import { useState, useEffect, useCallback } from 'react'
import {
  type ColumnFiltersState,
  type PaginationState,
} from '@tanstack/react-table'

type Props = {
  search: Record<string, unknown>
  navigate: (opts: {
    search: Record<string, unknown>
    replace?: boolean
  }) => void
  defaultPageSize?: number
}

export function useTableUrlState({
  search,
  navigate,
  defaultPageSize = 10,
}: Props) {
  // 1️⃣ Inicializamos estados locales desde la URL
  const [pagination, setPagination] = useState<PaginationState>(() => {
    const limit = Number(search.limit ?? defaultPageSize)
    const offset = Number(search.offset ?? 0)
    return {
      pageIndex: Math.floor(offset / limit),
      pageSize: limit,
    }
  })

  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(() => {
    return Object.entries(search)
      .filter(([key]) => !['limit', 'offset'].includes(key))
      .map(([id, value]) => ({ id, value }))
  })

  // 2️⃣ Efecto que actualiza URL cuando cambia pagination o filters
  useEffect(() => {
    const filtersObj = columnFilters.reduce(
      (acc, f) => ({ ...acc, [f.id]: f.value }),
      {}
    )

    navigate({
      search: {
        ...filtersObj,
        limit: pagination.pageSize,
        offset: pagination.pageIndex * pagination.pageSize,
      },
      replace: true,
    })
  }, [pagination, columnFilters, navigate])

  // 3️⃣ Funciones para actualizar estados (compatibles con react-table)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onPaginationChange = useCallback((updater: any) => {
    setPagination((prev) =>
      typeof updater === 'function' ? updater(prev) : updater
    )
  }, [])

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onColumnFiltersChange = useCallback((updater: any) => {
    setColumnFilters((prev) =>
      typeof updater === 'function' ? updater(prev) : updater
    )
  }, [])

  return {
    pageSize: pagination.pageSize,
    pageIndex: pagination.pageIndex,
    columnFilters,
    pagination,
    setPagination,
    setColumnFilters,
    onPaginationChange,
    onColumnFiltersChange,
  }
}
