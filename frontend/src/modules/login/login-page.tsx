import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import imageLoginPNG from "@/assets/images/image-login.png";
import { useLoginMutation } from "@/store/apis/auth.api";
import { toast } from "sonner";
import { useAppDispatch } from "@/store/store";
import { Loader2Icon } from "lucide-react";
import { loginUser } from "@/store/features/auth";
import { useNavigate } from "react-router-dom";
import { PATHS } from "@/constant/paths";

const loginSchema = z.object({
  identification: z
    .string({ message: "Este campo es requerido" })
    .min(1, { message: "Este campo es requerido" }),
  password: z
    .string({ message: "Este campo es requerido" })
    .min(1, { message: "Este campo es requerido" }),
});

type LoginSchema = z.infer<typeof loginSchema>;

export default function LoginPage() {
  //router
  const navigate = useNavigate();

  // hooks
  const dispatch = useAppDispatch();

  // form
  const form = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      identification: "",
      password: "",
    },
  });

  // mutations
  const [loginMutation, { isLoading }] = useLoginMutation();

  // methods
  function onSubmit(values: LoginSchema) {
    loginMutation(values)
      .unwrap()
      .then((data) => {
        dispatch(
          loginUser({
            token: data.token,
            user: data.employee,
          })
        );
        toast.success("Inicio de sesión exitoso", {
          description: "Bienvenido a PPS",
        });
        navigate(PATHS.HOME);
      })
      .catch(() => {
        toast.error("Error", {
          description: "Error al iniciar sesión, revise sus credenciales",
        });
      });
  }

  return (
    <div className="bg-muted flex min-h-svh flex-col items-center justify-center p-6 md:p-10">
      <div className="w-full max-w-sm md:max-w-3xl">
        <div className={"flex flex-col gap-6"}>
          <Card className="overflow-hidden p-0">
            <CardContent className="grid min-h-[400px] p-0 md:grid-cols-2">
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="p-6 md:p-8"
                >
                  <div className="flex flex-col gap-6">
                    <div className="flex flex-col items-center text-center">
                      <h1 className="text-2xl font-bold">Bienvenido a PPS</h1>
                      <p className="text-muted-foreground text-balance">
                        Inicia sesión para continuar
                      </p>
                    </div>
                    <div className="grid gap-3">
                      <FormField
                        control={form.control}
                        name="identification"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Identificación</FormLabel>
                            <FormControl>
                              <Input
                                disabled={isLoading}
                                placeholder="12345678"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                    <div className="grid gap-3">
                      <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Contraseña</FormLabel>
                            <FormControl>
                              <Input
                                disabled={isLoading}
                                type="password"
                                placeholder="********"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                    <Button
                      disabled={isLoading}
                      type="submit"
                      className="w-full"
                    >
                      {isLoading && <Loader2Icon className="animate-spin" />}
                      Iniciar sesión
                    </Button>
                  </div>
                </form>
              </Form>
              <div className="bg-muted relative hidden md:block">
                <img
                  src={imageLoginPNG}
                  alt="Image"
                  className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
                />
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
