import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { objectToFormData } from "@/helper/object-to-formdata";
import type {
  CreateEmployeeDto,
  Employee,
  OOOTypesResponse,
  OOOType,
  CreateOooDto,
  CreateOooResponse,
  OOOModel,
  GetRolesResponse,
  UpdateEmployeeDto,
  GetEmployeesParams,
  GetEmployeesResponse,
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
    getEmployeeById: builder.query<Employee, number>({
      query: (id) => ({
        url: `/employees/${id}/`,
      }),
      providesTags: ["employees"],
    }),
    createEmployee: builder.mutation<Employee, CreateEmployeeDto>({
      query: (body) => ({
        url: "/employees/",
        method: "POST",
        body,
      }),
      invalidatesTags: ["employees"],
    }),
    updateEmployee: builder.mutation<Employee, UpdateEmployeeDto>({
      query: ({ id, ...body }) => ({
        url: `/employees/${id}/`,
        method: "PUT",
        body,
      }),
      invalidatesTags: ["employees"],
    }),
    // ooo
    getAllOoo: builder.query<OOOModel[], void>({
      query: () => ({
        url: "/employees/list_ooo/",
      }),
      providesTags: ["ooo"],
    }),
    createOoo: builder.mutation<CreateOooResponse, CreateOooDto>({
      query: (body) => ({
        url: "/employees/create_ooo/",
        method: "POST",
        body: objectToFormData(body),
      }),
      invalidatesTags: ["ooo"],
    }),
    deleteOoo: builder.mutation<CreateOooResponse, number>({
      query: (id) => ({
        url: `/employees/delete_ooo/${id}`,
        method: "DELETE",
      }),
      invalidatesTags: ["ooo"],
    }),
    getAllOooTypes: builder.query<OOOType[], void>({
      query: () => ({
        url: "/employees/ooo_types/",
      }),
      transformResponse(oooTypes: OOOTypesResponse) {
        const data: OOOType[] = [];

        for (const p in oooTypes) {
          const key = p as keyof OOOTypesResponse;
          data.push({
            id: key,
            label: oooTypes[key],
          });
        }

        return data;
      },
    }),
  }),
});

export const {
  // employees
  useGetRolesQuery,
  useGetEmployeesQuery,
  useGetEmployeeByIdQuery,
  useCreateEmployeeMutation,
  // ooo
  useGetAllOooQuery,
  useGetAllOooTypesQuery,
  useCreateOooMutation,
  useDeleteOooMutation,
} = employeesApi;
