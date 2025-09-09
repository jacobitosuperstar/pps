import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { queryClient } from '@/main'
import { toast } from 'sonner'
import createEmployeeMutation from '@/api/employees/mutations/create-employee'
import updateEmployeeMutation from '@/api/employees/mutations/update-employee'
import { type Employee } from '@/api/employees/queries/employees'
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
import { PasswordInput } from '@/components/password-input'
import { SelectDropdown } from '@/components/select-dropdown'
import { roles } from '../data/data'

const formSchema = z.object({
  identification: z.string().min(1, 'Identificación es requerida.'),
  names: z.string().min(1, 'Nombres es requerido.'),
  last_names: z.string().min(1, 'Apellidos es requerido.'),
  role: z.string().min(1, 'Rol es requerido.'),
  birthday: z.string().min(1, 'Cumpleaños es requerido.'),
  password: z
    .string()
    .min(8, 'La contraseña debe tener al menos 8 caracteres.'),
})

type EmployeeForm = z.infer<typeof formSchema>

type EmployeeActionDialogProps = {
  currentRow?: Employee
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function EmployeesActionDialog({
  currentRow,
  open,
  onOpenChange,
}: EmployeeActionDialogProps) {
  const isEdit = !!currentRow
  const form = useForm<EmployeeForm>({
    resolver: zodResolver(formSchema),
    defaultValues: isEdit
      ? {
          identification: currentRow?.identification ?? '',
          names: currentRow?.names ?? '',
          last_names: currentRow?.last_names ?? '',
          role: currentRow?.role ?? '',
          birthday: currentRow?.birthday ?? '',
          password: '',
        }
      : {
          identification: '',
          names: '',
          last_names: '',
          role: '',
          birthday: '',
          password: '',
        },
  })

  const createMutation = useMutation({
    mutationFn: (payload: EmployeeForm) => createEmployeeMutation(payload),
    onSuccess: () => {
      toast.success('Empleado creado exitosamente')
      form.reset()
      queryClient.invalidateQueries({ queryKey: ['employees'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al crear el empleado')
    },
  })

  const updateMutation = useMutation({
    mutationFn: (payload: EmployeeForm) => updateEmployeeMutation(payload),
    onSuccess: () => {
      toast.success('Empleado actualizado exitosamente')
      form.reset()
      queryClient.invalidateQueries({ queryKey: ['employees'] })
      onOpenChange(false)
    },
    onError: () => {
      toast.error('Error al crear el empleado')
    },
  })

  const isLoading = createMutation.isPending || updateMutation.isPending

  const onSubmit = (values: EmployeeForm) => {
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
            {isEdit ? 'Editar Empleado' : 'Agregar Nuevo Empleado'}
          </DialogTitle>
          <DialogDescription>
            {isEdit
              ? 'Actualiza la información del empleado aquí. '
              : 'Crea un nuevo empleado aquí. '}
            Haz clic en guardar cuando termines.
          </DialogDescription>
        </DialogHeader>
        <div className='h-[26.25rem] w-[calc(100%+0.75rem)] overflow-y-auto py-1 pe-3'>
          <Form {...form}>
            <form
              id='user-form'
              onSubmit={form.handleSubmit(onSubmit)}
              className='space-y-4 px-0.5'
            >
              <FormField
                control={form.control}
                name='identification'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Identificación
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
                name='names'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Nombres
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        placeholder='Juan'
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
                name='last_names'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Apellidos
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        placeholder='Perez'
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
                name='role'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>Rol</FormLabel>
                    <SelectDropdown
                      defaultValue={field.value}
                      onValueChange={field.onChange}
                      disabled={isLoading}
                      placeholder='Selecciona un rol'
                      className='col-span-4'
                      items={roles.map(({ label, value }) => ({
                        label,
                        value,
                      }))}
                    />
                    <FormMessage className='col-span-4 col-start-3' />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name='birthday'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Cumpleaños
                    </FormLabel>
                    <FormControl>
                      <Input
                        disabled={isLoading}
                        type='date'
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
                name='password'
                render={({ field }) => (
                  <FormItem className='grid grid-cols-6 items-center space-y-0 gap-x-4 gap-y-1'>
                    <FormLabel className='col-span-2 text-end'>
                      Contraseña
                    </FormLabel>
                    <FormControl>
                      <PasswordInput
                        disabled={isLoading}
                        placeholder='e.g., S3cur3P@ssw0rd'
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
            form='user-form'
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
