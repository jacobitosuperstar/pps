import { AddEmployeeForm } from "../components/add-employee-form";

export default function CreateEmployeePage() {
  return (
    <div className="container max-w-2xl py-10 mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Agregar empleado</h1>
        <p className="text-muted-foreground mt-2">
          Agregar un nuevo empleado a tu empresa.
        </p>
      </div>
      <AddEmployeeForm />
    </div>
  );
}
