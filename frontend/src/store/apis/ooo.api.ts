import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import type {
  CreateOOODTO,
  GetOOOResponse,
  OOO,
  OOOTypesResponse,
  UpdateOOODTO,
  GetOOOParams,
} from "@/interfaces/ooo.interface";

export const OOOApi = createApi({
  reducerPath: "OOOApi",
  baseQuery: appBaseQuery,
  tagTypes: ["ooo"],
  endpoints: (builder) => ({
    // employees
    getOOOTypes: builder.query<OOOTypesResponse, void>({
      query: () => "/ooo/types/",
    }),
    getAllOOO: builder.query<GetOOOResponse, GetOOOParams>({
      query: (params) => ({
        url: "/ooo/",
        params,
      }),
      providesTags: ["ooo"],
    }),
    getOOOById: builder.query<OOO, number>({
      query: (id) => ({
        url: `/ooo/${id}/`,
      }),
      providesTags: ["ooo"],
    }),
    createOOO: builder.mutation<OOO, CreateOOODTO>({
      query: (body) => ({
        url: "/ooo/",
        method: "POST",
        body,
      }),
      invalidatesTags: ["ooo"],
    }),
    updateOOO: builder.mutation<OOO, UpdateOOODTO>({
      query: ({ id, ...body }) => ({
        url: `/ooo/${id}/`,
        method: "PUT",
        body,
      }),
      invalidatesTags: ["ooo"],
    }),
  }),
});

export const {
  useGetOOOTypesQuery,
  useGetAllOOOQuery,
  useGetOOOByIdQuery,
  useCreateOOOMutation,
  useUpdateOOOMutation,
} = OOOApi;
