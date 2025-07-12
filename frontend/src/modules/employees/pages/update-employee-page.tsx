import { PATHS } from "@/constant/paths";
import { useGetEmployeeByIdQuery } from "@/store/apis/employees.api";
import { Navigate, useParams } from "react-router-dom";
import { UpdateEmployeeForm } from "../components/update-employee-form";
import { Loader2Icon } from "lucide-react";

export default function UpdateEmployeePage() {
  const { id } = useParams();
  const employeeId = Number(id);

  const { data: employee, isLoading } = useGetEmployeeByIdQuery(employeeId, {
    skip: Number.isNaN(employeeId),
  });

  if (Number.isNaN(employeeId)) {
    return <Navigate to={PATHS.EMPLOYEES.INDEX} />;
  }
  console.log(employee);

  return (
    <div className="container max-w-2xl py-10 mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">
          Actualizar empleado
        </h1>
        <p className="text-muted-foreground mt-2">
          Actualizar datos de un empleado.
        </p>
      </div>
      {isLoading || !employee ? (
        <div className="flex items-center justify-center h-64">
          <Loader2Icon className="animate-spin" />
        </div>
      ) : (
        <UpdateEmployeeForm employeeId={employeeId} currentValues={employee} />
      )}
    </div>
  );
}
