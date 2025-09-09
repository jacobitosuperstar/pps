import { UserPlus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useEmployee } from './employees-provider'

export function EmployeesPrimaryButtons() {
  const { setOpen } = useEmployee()
  return (
    <div className='flex gap-2'>
      <Button className='space-x-1' onClick={() => setOpen('add')}>
        <span>Agregar Empleado</span> <UserPlus size={18} />
      </Button>
    </div>
  )
}
