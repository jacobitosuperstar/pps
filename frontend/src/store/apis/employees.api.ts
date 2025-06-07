import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import type {
  CreateEmployeeDTO,
  Employee,
  GetRolesResponse,
  UpdateEmployeeDTO,
  GetEmployeesParams,
  GetEmployeesResponse,
  GetOptionsResponse,
} from "@/interfaces/employees.interface";

export const employeesApi = createApi({
  reducerPath: "employeesApi",
  baseQuery: appBaseQuery,
  tagTypes: ["employees", "ooo"],
  endpoints: (builder) => ({
    // employees
    getRoles: builder.query<GetRolesResponse, void>({
      query: () => "/employees/roles/",
    }),
    getEmployees: builder.query<GetEmployeesResponse, GetEmployeesParams>({
      query: (params) => ({
        url: "/employees/",
        params,
      }),
      providesTags: ["employees"],
    }),
    getEmployeesOptions: builder.infiniteQuery<
      GetOptionsResponse,
      GetEmployeesParams,
      number
    >({
      query: ({ pageParam, queryArg: { search, page_size } }) => ({
        url: "/employees/options/",
        params: {
          page: pageParam,
          search: search || undefined,
          page_size,
        },
      }),
      providesTags: ["employees"],
      infiniteQueryOptions: {
        initialPageParam: 1,
        getNextPageParam: (res) =>
          res.next ? Number(res.next.split("?")[1].split("=")[1]) : undefined,
        getPreviousPageParam: (res) =>
          res.previous
            ? Number(res.previous.split("?")[1].split("=")[1])
            : undefined,
      },
    }),
    getEmployeeById: builder.query<Employee, number>({
      query: (id) => ({
        url: `/employees/${id}/`,
      }),
      providesTags: ["employees"],
    }),
    createEmployee: builder.mutation<Employee, CreateEmployeeDTO>({
      query: (body) => ({
        url: "/employees/",
        method: "POST",
        body,
      }),
      invalidatesTags: ["employees"],
    }),
    updateEmployee: builder.mutation<Employee, UpdateEmployeeDTO>({
      query: ({ id, ...body }) => ({
        url: `/employees/${id}/`,
        method: "PUT",
        body,
      }),
      invalidatesTags: ["employees"],
    }),
    deactivateEmployee: builder.mutation<Employee, number>({
      query: (id) => ({
        url: `/employees/${id}/deactivate/`,
        method: "POST",
      }),
      invalidatesTags: ["employees"],
    }),
  }),
});

export const {
  useGetRolesQuery,
  useGetEmployeesQuery,
  useGetEmployeeByIdQuery,
  useLazyGetEmployeeByIdQuery,
  useCreateEmployeeMutation,
  useUpdateEmployeeMutation,
  useDeactivateEmployeeMutation,
  useGetEmployeesOptionsInfiniteQuery,
} = employeesApi;
