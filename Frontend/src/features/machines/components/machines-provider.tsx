import React, { useState } from 'react'
import { type Machine } from '@/api/machines/queries/get-machines'
import useDialogState from '@/hooks/use-dialog-state'

type MachineDialogType = 'add' | 'edit' | 'delete'

type MachineContextType = {
  open: MachineDialogType | null
  setOpen: (str: MachineDialogType | null) => void
  currentRow: Machine | null
  setCurrentRow: React.Dispatch<React.SetStateAction<Machine | null>>
}

const MachineContext = React.createContext<MachineContextType | null>(null)

export function MachineProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useDialogState<MachineDialogType>(null)
  const [currentRow, setCurrentRow] = useState<Machine | null>(null)

  return (
    <MachineContext value={{ open, setOpen, currentRow, setCurrentRow }}>
      {children}
    </MachineContext>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useMachine = () => {
  const machineContext = React.useContext(MachineContext)

  if (!machineContext) {
    throw new Error('useMachine has to be used within <MachineContext>')
  }

  return machineContext
}
