import { UserPlus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useMachine } from './machines-provider'

export function MachinesPrimaryButtons() {
  const { setOpen } = useMachine()
  return (
    <div className='flex gap-2'>
      <Button className='space-x-1' onClick={() => setOpen('add')}>
        <span>Agregar Máquina</span> <UserPlus size={18} />
      </Button>
    </div>
  )
}
