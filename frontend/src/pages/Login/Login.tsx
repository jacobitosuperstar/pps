import {
  Avatar,
  Box,
  Checkbox,
  FormControlLabel,
  Grid,
  Link,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import LoadingButton from "@mui/lab/LoadingButton";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import LoginBgTeal from "@/assets/images/login-bg-teal.webp";
import { useAppDispatch, useAppSelector } from "@/store";
import { Navigate } from "react-router-dom";
import { PATHS } from "@/constants";
import { z } from "zod";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginUser } from "@/store/features/auth";
import { useLoginMutation } from "@/store/apis";
import { useEffect } from "react";

const schema = z
  .object({
    identification: z.string().min(1, "Este campo es requerido"),
    password: z.string().min(1, "Este campo es requerido"),
    remenberMe: z.boolean(),
  })
  .required();

type FormData = z.infer<typeof schema>;

const Login = () => {
  // redux
  const [doLogin, loginContext] = useLoginMutation();

  const dispatch = useAppDispatch();
  const authState = useAppSelector((state) => state.auth);
  // form control
  const { control, handleSubmit, setValue } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      identification: "",
      password: "",
      remenberMe: false,
    },
  });

  // methods
  const onSubmit = async (formData: FormData) => {
    try {
      let remenberedId = "";

      if (formData.remenberMe) {
        remenberedId = formData.identification;
      } else {
        remenberedId = "";
      }

      const response = await doLogin(formData).unwrap();

      dispatch(
        loginUser({
          token: response.token,
          remenberedId,
        })
      );
    } catch (error) {
      console.log(error);
    }
  };

  // effects
  useEffect(() => {
    setValue("identification", authState.remenberedId);
    setValue("remenberMe", !!authState.remenberedId);
  }, []);

  // validate auth
  if (authState.isAuthenticate) {
    return <Navigate to={PATHS.HOME}></Navigate>;
  }

  return (
    <Grid container component="main" sx={{ height: "100vh" }}>
      <Grid
        component="section"
        item
        xs={false}
        sm={4}
        md={7}
        sx={{
          backgroundImage: `url(${LoginBgTeal})`,
          backgroundRepeat: "no-repeat",
          backgroundColor: (t) =>
            t.palette.mode === "light"
              ? t.palette.grey[50]
              : t.palette.grey[900],
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      <Grid item xs={12} sm={8} md={5} component={Paper} elevation={6} square>
        <Box
          sx={{
            my: 8,
            mx: 4,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: "primary.main" }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Inicio de sesión
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit(onSubmit)}
            sx={{ mt: 1 }}
          >
            <Controller
              name="identification"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={loginContext.isLoading}
                  margin="normal"
                  required
                  fullWidth
                  id="identification"
                  label="Identificación"
                  type="text"
                  autoFocus
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                />
              )}
            />

            <Controller
              name="password"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <TextField
                  disabled={loginContext.isLoading}
                  margin="normal"
                  required
                  fullWidth
                  label="Contraseña"
                  type="password"
                  id="password"
                  autoComplete="current-password"
                  error={!!error}
                  helperText={error?.message}
                  {...field}
                />
              )}
            />

            <Controller
              name="remenberMe"
              control={control}
              render={({ field }) => (
                <FormControlLabel
                  control={
                    <Checkbox
                      color="primary"
                      onChange={(e) => field.onChange(e.target.checked)}
                      onBlur={(e) => field.onBlur(e.target.checked)}
                      checked={field.value}
                    />
                  }
                  label="Recuérdame"
                />
              )}
            />

            <LoadingButton
              loading={loginContext.isLoading}
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Ingresar
            </LoadingButton>
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  ¿Olvidaste tu contraseña?
                </Link>
              </Grid>
              <Grid item>
                <Link href="#" variant="body2">
                  ¿No tienes cuenta? Regístrate
                </Link>
              </Grid>
            </Grid>
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
};

export default Login;
