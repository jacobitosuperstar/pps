import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { LoginDto, LoginResponse } from "@/interfaces/auth.interface";
import { objectToFormData } from "@/helper/object-to-formdata";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: appBaseQuery,
  endpoints: (builder) => ({
    login: builder.mutation<LoginResponse, LoginDto>({
      query: (body) => ({
        url: "/employees/login/",
        method: "POST",
        body: objectToFormData(body),
      }),
    }),
  }),
});

export const { useLoginMutation } = authApi;
