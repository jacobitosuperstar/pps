import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/main'
import { AlertTriangle } from 'lucide-react'
import { toast } from 'sonner'
import deleteEmployeeMutation from '@/api/employees/mutations/delete-employee'
import { type Employee } from '@/api/employees/queries/employees'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ConfirmDialog } from '@/components/confirm-dialog'
import { roles } from '../data/data'

type EmployeeDeleteDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  currentRow: Employee
}

export function EmployeesDeleteDialog({
  open,
  onOpenChange,
  currentRow,
}: EmployeeDeleteDialogProps) {
  const [value, setValue] = useState('')

  const deleteMutation = useMutation({
    mutationFn: (payload: string) => {
      return deleteEmployeeMutation(payload)
    },
    onSuccess: () => {
      toast.success('Empleado eliminado exitosamente')
      queryClient.invalidateQueries({ queryKey: ['employees'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al eliminar el empleado')
    },
  })

  const handleDelete = () => {
    if (value.trim() !== currentRow.identification) return

    deleteMutation.mutate(value)
  }

  return (
    <ConfirmDialog
      open={open}
      onOpenChange={onOpenChange}
      handleConfirm={handleDelete}
      disabled={value.trim() !== currentRow.identification}
      title={
        <span className='text-destructive'>
          <AlertTriangle
            className='stroke-destructive me-1 inline-block'
            size={18}
          />{' '}
          Eliminar Empleado
        </span>
      }
      desc={
        <div className='space-y-4'>
          <p className='mb-2'>
            ¿Estás seguro de eliminar{' '}
            <span className='font-bold'>{currentRow.identification}</span>?
            <br />
            Esta acción eliminará permanentemente el usuario con el rol de{' '}
            <span className='font-bold'>
              {roles.find((role) => role.value === currentRow.role)?.label}
            </span>{' '}
            del sistema. Esta acción no puede ser deshecha.
          </p>

          <Label className='my-2'>
            Identificación:
            <Input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder='Enter identification to confirm deletion.'
            />
          </Label>

          <Alert variant='destructive'>
            <AlertTitle>Advertencia!</AlertTitle>
            <AlertDescription>
              Por favor, ten cuidado, esta operación no puede ser deshecha.
            </AlertDescription>
          </Alert>
        </div>
      }
      confirmText='Eliminar'
      destructive
    />
  )
}
