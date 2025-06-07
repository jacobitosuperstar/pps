import { useConfirm } from "@/components/providers/confirm-provider";
import { Button } from "@/components/ui/button";
import { useDeactivateEmployeeMutation } from "@/store/apis/employees.api";
import { Loader2Icon, Trash } from "lucide-react";

interface Props {
  employeeId: number;
}

export const DeleteButton = ({ employeeId }: Props) => {
  const confirm = useConfirm();
  const [deactivateEmployee, { isLoading: isDeactivatingEmployee }] =
    useDeactivateEmployeeMutation();

  const handleDelete = async () => {
    const result = await confirm({
      title: "Eliminar empleado",
      description: "¿Estás seguro de eliminar este empleado?",
      confirmText: "Eliminar",
      cancelText: "Cancelar",
    });

    if (result) {
      await deactivateEmployee(employeeId);
    }
  };

  return (
    <Button
      disabled={isDeactivatingEmployee}
      variant="default"
      size="icon"
      className="size-8"
      onClick={() => handleDelete()}
    >
      {isDeactivatingEmployee ? (
        <Loader2Icon className="animate-spin" />
      ) : (
        <Trash />
      )}
    </Button>
  );
};
