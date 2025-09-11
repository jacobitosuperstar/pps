import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/main'
import { AlertTriangle } from 'lucide-react'
import { toast } from 'sonner'
import deleteClientMutation from '@/api/clients/mutations/delete-client'
import { type Client } from '@/api/clients/queries/get-clients'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { ConfirmDialog } from '@/components/confirm-dialog'

type ClientsDeleteDialogProps = {
  open: boolean
  onOpenChange: (open: boolean) => void
  currentRow: Client
}

export function ClientsDeleteDialog({
  open,
  onOpenChange,
  currentRow,
}: ClientsDeleteDialogProps) {
  const [value, setValue] = useState('')

  const deleteMutation = useMutation({
    mutationFn: (payload: string) => {
      return deleteClientMutation(payload)
    },
    onSuccess: () => {
      toast.success('Cliente eliminado exitosamente')
      queryClient.invalidateQueries({ queryKey: ['clients'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al eliminar el cliente')
    },
  })

  const handleDelete = () => {
    if (value.trim() !== currentRow.client_id) return

    deleteMutation.mutate(value)
  }

  return (
    <ConfirmDialog
      open={open}
      onOpenChange={onOpenChange}
      handleConfirm={handleDelete}
      disabled={value.trim() !== currentRow.client_id}
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
            <span className='font-bold'>{currentRow.client_id}</span>?
            <br />
            Esta acción eliminará permanentemente el cliente del sistema. Esta
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
