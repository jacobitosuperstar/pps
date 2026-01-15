import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/main'
import { AlertTriangle } from 'lucide-react'
import { toast } from 'sonner'
import deleteMachineMutation from '@/api/machines/mutations/delete-machine'
import { type Machine } from '@/api/machines/queries/get-machines'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ConfirmDialog } from '@/components/confirm-dialog'

type MachinesDeleteDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  currentRow: Machine
}

export function MachinesDeleteDialog({
  open,
  onOpenChange,
  currentRow,
}: MachinesDeleteDialogProps) {
  const [value, setValue] = useState('')

  const deleteMutation = useMutation({
    mutationFn: (payload: string) => {
      return deleteMachineMutation(payload)
    },
    onSuccess: () => {
      toast.success('Máquina eliminada exitosamente')
      queryClient.invalidateQueries({ queryKey: ['machines'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al eliminar la máquina')
    },
  })

  const handleDelete = () => {
    if (value.trim() !== currentRow.id.toString()) return

    deleteMutation.mutate(value)
  }

  return (
    <ConfirmDialog
      open={open}
      onOpenChange={onOpenChange}
      handleConfirm={handleDelete}
      disabled={value.trim() !== currentRow.id.toString()}
      title={
        <span className='text-destructive'>
          <AlertTriangle
            className='stroke-destructive me-1 inline-block'
            size={18}
          />{' '}
          Eliminar Cliente
        </span>
      }
      desc={
        <div className='space-y-4'>
          <p className='mb-2'>
            ¿Estás seguro de eliminar{' '}
            <span className='font-bold'>{currentRow.id}</span>?
            <br />
            Esta acción eliminará permanentemente la máquina del sistema. Esta
            acción no puede ser deshecha.
          </p>

          <Label className='my-2'>
            Identificación del cliente:
            <Input
              value={value}
              onChange={(e) => setValue(e.target.value)}
              placeholder='Ingrese la identificación para confirmar la eliminación.'
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
