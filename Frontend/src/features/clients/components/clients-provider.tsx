import React, { useState } from 'react'
import { type Client } from '@/api/clients/queries/get-clients'
import useDialogState from '@/hooks/use-dialog-state'

type ClientDialogType = 'add' | 'edit' | 'delete'

type ClientContextType = {
  open: ClientDialogType | null
  setOpen: (str: ClientDialogType | null) => void
  currentRow: Client | null
  setCurrentRow: React.Dispatch<React.SetStateAction<Client | null>>
}

const ClientContext = React.createContext<ClientContextType | null>(null)

export function ClientProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useDialogState<ClientDialogType>(null)
  const [currentRow, setCurrentRow] = useState<Client | null>(null)

  return (
    <ClientContext value={{ open, setOpen, currentRow, setCurrentRow }}>
      {children}
    </ClientContext>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useClient = () => {
  const clientContext = React.useContext(ClientContext)

  if (!clientContext) {
    throw new Error('useClient has to be used within <ClientContext>')
  }

  return clientContext
}
