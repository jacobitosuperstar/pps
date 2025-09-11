import { UserPlus } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useClient } from './clients-provider'

export function ClientsPrimaryButtons() {
  const { setOpen } = useClient()
  return (
    <div className='flex gap-2'>
      <Button className='space-x-1' onClick={() => setOpen('add')}>
        <span>Agregar Cliente</span> <UserPlus size={18} />
      </Button>
    </div>
  )
}
