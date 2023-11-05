import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";

export const authApi = createApi({
  reducerPath: "authApi",
  baseQuery: appBaseQuery,
  endpoints: (builder) => ({
    login: builder.mutation({
      query: () => ({
        url: "/login",
      }),
    }),
  }),
});

export const { useLoginMutation } = authApi;
