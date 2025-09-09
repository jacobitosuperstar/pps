import { useNavigate, useLocation } from '@tanstack/react-router'
import { useAuthStore } from '@/stores/auth-store'
import { ConfirmDialog } from '@/components/confirm-dialog'

interface SignOutDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function SignOutDialog({ open, onOpenChange }: SignOutDialogProps) {
  const navigate = useNavigate()
  const location = useLocation()
  const { auth } = useAuthStore()

  const handleSignOut = () => {
    auth.reset()
    // Guardar la ruta actual para redirigir después del inicio de sesión
    const currentPath = location.href
    navigate({
      to: '/sign-in',
      search: { redirect: currentPath },
      replace: true,
    })
  }

  return (
    <ConfirmDialog
      open={open}
      onOpenChange={onOpenChange}
      title='Cerrar sesión'
      desc='¿Estás seguro de que deseas cerrar sesión? Necesitarás iniciar sesión nuevamente para acceder al sistema.'
      confirmText='Cerrar sesión'
      handleConfirm={handleSignOut}
      className='sm:max-w-sm'
    />
  )
}
