import {
  Avatar,
  Box,
  Button,
  Checkbox,
  FormControlLabel,
  Grid,
  Link,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import LockOutlinedIcon from "@mui/icons-material/LockOutlined";
import LoginBgTeal from "@/assets/images/login-bg-teal.webp";
import { useAppDispatch, useAppSelector } from "@/store";
import { Navigate } from "react-router-dom";
import { PATHS } from "@/constants";
import { z } from "zod";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginUser } from "@/store/features/auth";
import { useLoginMutation, usePinQuery } from "@/store/apis";

const schema = z
  .object({
    identification: z.string().min(1, "Este campo es requerido"),
    password: z.string().min(1, "Este campo es requerido"),
  })
  .required();

type FormData = z.infer<typeof schema>;

const Login = () => {
  // redux
  usePinQuery();
  const [doLogin, loginContext] = useLoginMutation();
  const isAuthenticate = useAppSelector((state) => state.auth.isAuthenticate);
  const dispatch = useAppDispatch();
  // form control
  const { control, handleSubmit } = useForm<FormData>({
    resolver: zodResolver(schema),
    defaultValues: {
      identification: "",
      password: "",
    },
  });

  // methods
  const onSubmit = async (formData: FormData) => {
    try {
      const response = doLogin(formData).unwrap();

      console.log(response);
    } catch (error) {
      console.log(error);
    }

    // dispatch(loginUser(1));
  };
  // validate auth
  if (isAuthenticate) {
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

            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Recuérdame"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Ingresar
            </Button>
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
