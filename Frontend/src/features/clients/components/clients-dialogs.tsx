import { ClientsActionDialog } from './clients-action-dialog'
import { ClientsDeleteDialog } from './clients-delete-dialog'
import { useClient } from './clients-provider'

export function ClientDialogs() {
  const { open, setOpen, currentRow, setCurrentRow } = useClient()
  return (
    <>
      <ClientsActionDialog
        key='client-add'
        open={open === 'add'}
        onOpenChange={() => setOpen('add')}
      />

      {currentRow && (
        <>
          <ClientsActionDialog
            key={`client-edit-${currentRow.client_id}`}
            open={open === 'edit'}
            onOpenChange={() => {
              setOpen('edit')
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
            }}
            currentRow={currentRow}
          />

          <ClientsDeleteDialog
            key={`client-delete-${currentRow.client_id}`}
            open={open === 'delete'}
            onOpenChange={() => {
              setOpen('delete')
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
            }}
            currentRow={currentRow}
          />
        </>
      )}
    </>
  )
}
