import { MachinesActionDialog } from './machines-action-dialog'
import { MachinesDeleteDialog } from './machines-delete-dialog'
import { useMachine } from './machines-provider'

export function MachinesDialogs() {
  const { open, setOpen, currentRow, setCurrentRow } = useMachine()
  return (
    <>
      <MachinesActionDialog
        key='machine-add'
        open={open === 'add'}
        onOpenChange={() => setOpen('add')}
      />

      {currentRow && (
        <>
          <MachinesActionDialog
            key={`machine-edit-${currentRow.id}`}
            open={open === 'edit'}
            onOpenChange={() => {
              setOpen('edit')
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
            }}
            currentRow={currentRow}
          />

          <MachinesDeleteDialog
            key={`machine-delete-${currentRow.id}`}
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
