import React, { useState } from 'react'
import { type Employee } from '@/api/employees/queries/employees'
import useDialogState from '@/hooks/use-dialog-state'

type EmployeeDialogType = 'invite' | 'add' | 'edit' | 'delete'

type EmployeeContextType = {
  open: EmployeeDialogType | null
  setOpen: (str: EmployeeDialogType | null) => void
  currentRow: Employee | null
  setCurrentRow: React.Dispatch<React.SetStateAction<Employee | null>>
}

const EmployeeContext = React.createContext<EmployeeContextType | null>(null)

export function EmployeeProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useDialogState<EmployeeDialogType>(null)
  const [currentRow, setCurrentRow] = useState<Employee | null>(null)

  return (
    <EmployeeContext value={{ open, setOpen, currentRow, setCurrentRow }}>
      {children}
    </EmployeeContext>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useEmployee = () => {
  const employeeContext = React.useContext(EmployeeContext)

  if (!employeeContext) {
    throw new Error('useEmployee has to be used within <EmployeeContext>')
  }

  return employeeContext
}
