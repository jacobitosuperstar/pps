import { PATHS } from "@/constant/paths";
import { Navigate, useParams } from "react-router-dom";
import { useGetOOOByIdQuery } from "@/store/apis/ooo.api";
import { UpdateOooForm } from "../components/update-ooo-form";
import { Loader2Icon } from "lucide-react";

export default function UpdateOOOPage() {
  const { id } = useParams();
  const oooId = Number(id);

  const { data: ooo, isLoading } = useGetOOOByIdQuery(oooId, {
    skip: Number.isNaN(oooId),
  });

  if (Number.isNaN(oooId)) {
    return <Navigate to={PATHS.OOO.INDEX} />;
  }

  return (
    <div className="container max-w-2xl py-10 mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">
          Actualizar permiso
        </h1>
        <p className="text-muted-foreground mt-2">
          Genera un nuevo permiso para un empleado.
        </p>
      </div>
      {isLoading || !ooo ? (
        <div className="flex items-center justify-center h-64">
          <Loader2Icon className="animate-spin" />
        </div>
      ) : (
        <UpdateOooForm oooId={oooId} currentValues={ooo} />
      )}
    </div>
  );
}
