import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/main'
import { toast } from 'sonner'
import createMachineMutation from '@/api/machines/mutations/create-machine'
import updateMachineMutation from '@/api/machines/mutations/update-machine'
import { type Machine } from '@/api/machines/queries/get-machines'
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'

const formSchema = z.object({
  machine_code: z.string().min(1, 'El código de la máquina es requerido.'),
  name: z.string().min(1, 'El nombre es requerido.'),
  machine_type: z.string().optional(),
  status: z.enum(['active', 'inactive', 'maintenance']).default('active'),
  location: z.string().optional(),
  description: z.string().optional(),
  manufacturer: z.string().optional(),
  model: z.string().optional(),
  serial_number: z.string().optional(),
  installation_date: z.string().optional(),
  last_maintenance: z.string().optional(),
  next_maintenance: z.string().optional(),
})

type MachineForm = z.infer<typeof formSchema>

type MachineActionDialogProps = {
  currentRow?: Machine
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function MachinesActionDialog({
  currentRow,
  open,
  onOpenChange,
}: MachineActionDialogProps) {
  const isEdit = !!currentRow

  const form = useForm<MachineForm>({
    resolver: zodResolver(formSchema),
    defaultValues: isEdit
      ? {
          machine_code: currentRow?.machine_code || '',
          name: currentRow?.name || '',
          machine_type: currentRow?.machine_type || '',
          status: currentRow?.status || 'active',
          location: currentRow?.location || '',
          description: currentRow?.description || '',
          manufacturer: currentRow?.manufacturer || '',
          model: currentRow?.model || '',
          serial_number: currentRow?.serial_number || '',
          installation_date: currentRow?.installation_date || '',
          last_maintenance: currentRow?.last_maintenance || '',
          next_maintenance: currentRow?.next_maintenance || '',
        }
      : {
          machine_code: '',
          name: '',
          machine_type: '',
          status: 'active',
          location: '',
          description: '',
          manufacturer: '',
          model: '',
          serial_number: '',
          installation_date: '',
          last_maintenance: '',
          next_maintenance: '',
        },
  })

  // 3. Mutaciones actualizadas para máquinas
  const createMutation = useMutation({
    mutationFn: createMachineMutation,
    onSuccess: () => {
      toast.success('Máquina creada exitosamente')
      form.reset()
      queryClient.invalidateQueries({ queryKey: ['machines'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al crear la máquina')
    },
  })

  const updateMutation = useMutation({
    mutationFn: (payload: MachineForm) => updateMachineMutation(payload),
    onSuccess: () => {
      toast.success('Máquina actualizada exitosamente')
      form.reset()
      queryClient.invalidateQueries({ queryKey: ['machines'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al actualizar la máquina')
    },
  })

  const isLoading = createMutation.isPending || updateMutation.isPending

  const onSubmit = (values: MachineForm) => {
    if (isEdit) {
      updateMutation.mutate(values)
    } else {
      createMutation.mutate(values)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className='sm:max-w-lg'>
        <DialogHeader className='text-start'>
          <DialogTitle>
            {isEdit ? 'Editar Máquina' : 'Agregar Nueva Máquina'}
          </DialogTitle>
          <DialogDescription>
            {isEdit
              ? 'Actualiza la información de la máquina aquí.'
              : 'Crea una nueva máquina aquí.'}{' '}
            Haz clic en guardar cuando termines.
          </DialogDescription>
        </DialogHeader>

        {/* 4. Contenido del formulario actualizado con los campos de la máquina */}
        <div className='max-h-[60vh] overflow-y-auto p-1'>
          <Form {...form}>
            <form
              id='machine-form'
              onSubmit={form.handleSubmit(onSubmit)}
              className='space-y-4'
            >
              <FormField
                name='machine_code'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Código de la Máquina</FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading || isEdit}
                        placeholder='ej. EQ-001'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='name'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Nombre</FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        placeholder='ej. Torno CNC'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='status'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Estado</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                      disabled={isLoading}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder='Selecciona un estado' />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value='active'>Activo</SelectItem>
                        <SelectItem value='inactive'>Inactivo</SelectItem>
                        <SelectItem value='maintenance'>
                          En Mantenimiento
                        </SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='description'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Descripción</FormLabel>
                    <FormControl>
                      <Textarea
                        disabled={isLoading}
                        placeholder='Añade una descripción de la máquina...'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='location'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Ubicación</FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        placeholder='ej. Bodega 2, Sección A'
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='manufacturer'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Fabricante</FormLabel>
                    <FormControl>
                      <Input disabled={isLoading} {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='model'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Modelo</FormLabel>
                    <FormControl>
                      <Input disabled={isLoading} {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='serial_number'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Número de Serie</FormLabel>
                    <FormControl>
                      <Input disabled={isLoading} {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='installation_date'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Fecha de Instalación</FormLabel>
                    <FormControl>
                      <Input type='date' disabled={isLoading} {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='last_maintenance'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Último Mantenimiento</FormLabel>
                    <FormControl>
                      <Input type='date' disabled={isLoading} {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                name='next_maintenance'
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Próximo Mantenimiento</FormLabel>
                    <FormControl>
                      <Input type='date' disabled={isLoading} {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </form>
          </Form>
        </div>

        <DialogFooter>
          <LoadingButton
            type='submit'
            form='machine-form'
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
