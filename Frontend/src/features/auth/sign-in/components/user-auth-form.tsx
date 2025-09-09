import { useRef } from 'react'
import { z } from 'zod'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { useMutation } from '@tanstack/react-query'
import { Link, useNavigate } from '@tanstack/react-router'
import { toast } from 'sonner'
import {
  loginMutation,
  type LoginPayload,
} from '@/api/employees/mutations/login'
import { useAuthStore } from '@/stores/auth-store'
import { cn } from '@/lib/utils'
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

const formSchema = z.object({
  identification: z
    .string({ message: 'Este campo es requerido' })
    .min(1, { message: 'Este campo es requerido' }),
  password: z
    .string({ message: 'Este campo es requerido' })
    .min(1, { message: 'Este campo es requerido' }),
})

interface UserAuthFormProps extends React.HTMLAttributes<HTMLFormElement> {
  redirectTo?: string
}

export function UserAuthForm({
  className,
  redirectTo,
  ...props
}: UserAuthFormProps) {
  // router
  const navigate = useNavigate({ from: '/sign-in' })

  // states
  const loadingToast = useRef<string | number>('')
  const { auth } = useAuthStore()

  // form
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      identification: '',
      password: '',
    },
  })

  // services
  const { mutate: login, isPending } = useMutation({
    mutationFn: (payload: LoginPayload) => {
      loadingToast.current = toast.loading('Iniciando sesión')
      return loginMutation(payload)
    },
    onSuccess: (data) => {
      toast.dismiss(loadingToast.current)
      auth.setUser(data.employee)
      auth.setAccessToken(data.token)
      toast.success(
        `Bienvenido: ${data.employee.names} ${data.employee.last_names}`
      )
      navigate({ to: '/' })
    },
    onError: () => {
      toast.dismiss(loadingToast.current)
      toast.error('Identificación o contraseña incorrecta')
    },
  })

  const onSubmit = (data: z.infer<typeof formSchema>) => {
    login({
      identification: data.identification,
      password: data.password,
    })
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className={cn('grid gap-3', className)}
        {...props}
      >
        <FormField
          control={form.control}
          name='identification'
          render={({ field }) => (
            <FormItem>
              <FormLabel>Identificación</FormLabel>
              <FormControl>
                <Input placeholder='Número de identificación' {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name='password'
          render={({ field }) => (
            <FormItem className='relative'>
              <FormLabel>Contraseña</FormLabel>
              <FormControl>
                <PasswordInput placeholder='********' {...field} />
              </FormControl>
              <FormMessage />
              <Link
                to='/forgot-password'
                className='text-muted-foreground absolute end-0 -top-0.5 text-sm font-medium hover:opacity-75'
              >
                ¿Olvidaste tu contraseña?
              </Link>
            </FormItem>
          )}
        />

        <LoadingButton
          className='mt-2'
          disabled={isPending}
          loading={isPending}
        >
          Iniciar Sesión
        </LoadingButton>
        {/* 
        <div className='relative my-2'>
          <div className='absolute inset-0 flex items-center'>
            <span className='w-full border-t' />
          </div>
          <div className='relative flex justify-center text-xs uppercase'>
            <span className='bg-background text-muted-foreground px-2'>
              O continúa con
            </span>
          </div>
        </div>

        <div className='grid grid-cols-2 gap-2'>
          <Button variant='outline' type='button' disabled={isLoading}>
            <IconGithub className='h-4 w-4' /> GitHub
          </Button>
          <Button variant='outline' type='button' disabled={isLoading}>
            <IconFacebook className='h-4 w-4' /> Facebook
          </Button>
        </div> */}
      </form>
    </Form>
  )
}
