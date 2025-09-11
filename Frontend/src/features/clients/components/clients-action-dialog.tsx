import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/main'
import { isValidPhoneNumber, parsePhoneNumber } from 'react-phone-number-input'
import { toast } from 'sonner'
import createClientMutation from '@/api/clients/mutations/create-client'
import updateClientMutation from '@/api/clients/mutations/update-client'
import { type Client } from '@/api/clients/queries/get-clients'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { LoadingButton } from '@/components/ui/loading-button'
import { PhoneInput } from '@/components/ui/phone-input'

const formSchema = z.object({
  client_id: z.string().min(1, 'Documento de identidad es requerido.'),
  client_name: z.string().min(1, 'Nombre del cliente es requerido.'),
  client_email: z.email('Correo inválido.'),
  phone: z.string().refine(isValidPhoneNumber, {
    message: 'Número de teléfono inválido.',
  }),
})

type ClientForm = z.infer<typeof formSchema>

type ClientActionDialogProps = {
  currentRow?: Client
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ClientsActionDialog({
  currentRow,
  open,
  onOpenChange,
}: ClientActionDialogProps) {
  const isEdit = !!currentRow

  const phone = currentRow?.client_phone_number
    ? `${currentRow.client_phone_code}${currentRow.client_phone_number}`
    : ''

  const form = useForm<ClientForm>({
    resolver: zodResolver(formSchema),
    defaultValues: isEdit
      ? {
          client_id: currentRow?.client_id ?? '',
          client_name: currentRow?.client_name ?? '',
          client_email: currentRow?.client_email ?? '',
          phone: phone,
        }
      : {
          client_id: '',
          client_name: '',
          client_email: '',
          phone: '',
        },
  })

  const createMutation = useMutation({
    mutationFn: (payload: ClientForm) => {
      const parsed = parsePhoneNumber(payload.phone)

      if (!parsed) {
        throw new Error('Número de teléfono inválido.')
      }

      return createClientMutation({
        client_id: payload.client_id,
        client_name: payload.client_name,
        client_email: payload.client_email,
        client_phone_code: '+' + parsed.countryCallingCode,
        client_phone_number: parsed.nationalNumber,
      })
    },
    onSuccess: () => {
      toast.success('Cliente creado exitosamente')
      form.reset()
      queryClient.invalidateQueries({ queryKey: ['clients'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al crear el cliente')
    },
  })

  const updateMutation = useMutation({
    mutationFn: (payload: ClientForm) => {
      const parsed = parsePhoneNumber(payload.phone)

      if (!parsed) {
        throw new Error('Número de teléfono inválido.')
      }

      return updateClientMutation({
        client_id: payload.client_id,
        client_name: payload.client_name,
        client_email: payload.client_email,
        client_phone_code: '+' + parsed.countryCallingCode,
        client_phone_number: parsed.nationalNumber,
      })
    },
    onSuccess: () => {
      toast.success('Cliente actualizado exitosamente')
      form.reset()
      queryClient.invalidateQueries({ queryKey: ['clients'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al actualizar el cliente')
    },
  })

  const isLoading = createMutation.isPending || updateMutation.isPending

  const onSubmit = (values: ClientForm) => {
    if (isEdit) {
      updateMutation.mutate(values)
    } else {
      createMutation.mutate(values)
    }
  }

  return (
    <Dialog
      open={open}
      onOpenChange={(state) => {
        form.reset()
        onOpenChange(state)
      }}
    >
      <DialogContent className='sm:max-w-lg'>
        <DialogHeader className='text-start'>
          <DialogTitle>
            {isEdit ? 'Editar Cliente' : 'Agregar Nuevo Cliente'}
          </DialogTitle>
          <DialogDescription>
            {isEdit
              ? 'Actualiza la información del cliente aquí.'
              : 'Crea un nuevo cliente aquí.'}{' '}
            Haz clic en guardar cuando termines.
          </DialogDescription>
        </DialogHeader>
        <div className='h-[26.25rem] w-[calc(100%+0.75rem)] overflow-y-auto py-1 pe-3'>
          <Form {...form}>
            <form
              id='client-form'
              onSubmit={form.handleSubmit(onSubmit)}
              className='space-y-4 px-0.5'
            >
              <FormField
                control={form.control}
                name='client_id'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Documento
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading || isEdit}
                        placeholder='123456789'
                        className='col-span-4'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='col-span-4 col-start-3' />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name='client_name'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Nombre
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        placeholder='Juan Perez'
                        className='col-span-4'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='col-span-4 col-start-3' />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name='client_email'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Correo
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        type='email'
                        placeholder='correo@ejemplo.com'
                        className='col-span-4'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='col-span-4 col-start-3' />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name='phone'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Teléfono
                    </FormLabel>
                    <FormControl>
                      <PhoneInput
                        disabled={isLoading}
                        placeholder='3001234567'
                        className='col-span-4'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage className='col-span-4 col-start-3' />
                  </FormItem>
                )}
              />
            </form>
          </Form>
        </div>
        <DialogFooter>
          <LoadingButton
            type='submit'
            form='client-form'
            loading={isLoading}
            disabled={isLoading}
          >
            Guardar cambios
          </LoadingButton>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
