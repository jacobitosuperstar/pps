import { EmployeesActionDialog } from './employees-action-dialog'
import { EmployeesDeleteDialog } from './employees-delete-dialog'
import { useEmployee } from './employees-provider'

export function EmployeeDialogs() {
  const { open, setOpen, currentRow, setCurrentRow } = useEmployee()
  return (
    <>
      <EmployeesActionDialog
        key='user-add'
        open={open === 'add'}
        onOpenChange={() => setOpen('add')}
      />

      {currentRow && (
        <>
          <EmployeesActionDialog
            key={`user-edit-${currentRow.identification}`}
            open={open === 'edit'}
            onOpenChange={() => {
              setOpen('edit')
              setTimeout(() => {
                setCurrentRow(null)
              }, 500)
            }}
            currentRow={currentRow}
          />

          <EmployeesDeleteDialog
            key={`user-delete-${currentRow.identification}`}
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
