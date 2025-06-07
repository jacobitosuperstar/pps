import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import type { LoginDTO, LoginResponse } from "@/interfaces/auth.interface";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: appBaseQuery,
  endpoints: (builder) => ({
    login: builder.mutation<LoginResponse, LoginDTO>({
      query: (body) => ({
        url: "/employees/login/",
        method: "POST",
        body,
      }),
    }),
  }),
});

export const { useLoginMutation } = authApi;
