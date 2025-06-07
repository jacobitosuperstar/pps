import { AddOooForm } from "../components/add-ooo-form";

export default function CreateOOOPage() {
  return (
    <div className="container max-w-2xl py-10 mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Agregar permiso</h1>
        <p className="text-muted-foreground mt-2">
          Genera un nuevo permiso para un empleado.
        </p>
      </div>
      <AddOooForm />
    </div>
  );
}
