import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import {
  LoginDto,
  LoginResponse,
  PinResponse,
} from "@/interfaces/auth.interface";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: appBaseQuery,
  endpoints: (builder) => ({
    login: builder.mutation<LoginResponse, LoginDto>({
      query: (body) => ({
        url: "/employees/login/",
        method: "POST",
        body,
      }),
    }),
    pin: builder.query<PinResponse, void>({
      query: () => ({
        url: "/new_pin/",
      }),
    }),
  }),
});

export const { useLoginMutation, usePinQuery } = authApi;
