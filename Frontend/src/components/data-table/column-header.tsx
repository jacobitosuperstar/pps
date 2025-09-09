import { type Column } from '@tanstack/react-table'
import { FilterIcon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

type DataTableColumnHeaderProps<TData, TValue> =
  React.HTMLAttributes<HTMLDivElement> & {
    column: Column<TData, TValue>
    children: React.ReactNode
    onClick?: () => void
  }

export function DataTableColumnHeader<TData, TValue>({
  column,
  children,
  className,
  onClick,
}: DataTableColumnHeaderProps<TData, TValue>) {
  if (!column.getCanFilter()) {
    return <div className={cn(className)}>{children}</div>
  }

  const hasFilter =
    column.getFilterValue() !== undefined && column.getFilterValue() !== ''

  return (
    <div className={cn('flex items-center justify-start gap-2', className)}>
      <div>{children}</div>
      <Button
        className={cn(
          'pointer-events-none opacity-0 transition-opacity group-hover:pointer-events-auto group-hover:opacity-100',
          hasFilter && 'pointer-events-auto opacity-100'
        )}
        variant='ghost'
        size='icon'
        onClick={onClick}
      >
        <FilterIcon className='h-4 w-4' />
      </Button>
    </div>
  )
}
