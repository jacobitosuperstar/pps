import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { objectToFormData } from "@/helper/object-to-formdata";
import {
  CreateEmployeeDto,
  CreateEmployeeResponse,
  Employee,
  Role,
  RolesObject,
  OOOTypesResponse,
  OOOType,
  CreateOooDto,
  CreateOooResponse,
  OOOModel,
} from "@/interfaces/employees.interface";

export const employeesApi = createApi({
  reducerPath: "employeesApi",
  baseQuery: appBaseQuery,
  tagTypes: ["employees", "ooo"],
  endpoints: (builder) => ({
    getRoles: builder.query<Role[], void>({
      query: () => "/employees/roles/",
      transformResponse(response: RolesObject) {
        if (!response) return [];

        return Object.keys(response).map((x) => {
          const key = x as keyof RolesObject;
          return {
            id: key,
            name: response[key] as string,
          };
        });
      },
    }),
    getEmployees: builder.query<Employee[], void>({
      query: () => ({
        url: "/employees/",
      }),
      transformResponse(response: any) {
        return response?.employess || [];
      },
      providesTags: ["employees"],
    }),
    createEmployee: builder.mutation<CreateEmployeeResponse, CreateEmployeeDto>(
      {
        query: (body) => ({
          url: "/employees/create_employee/",
          method: "POST",
          body: objectToFormData(body),
        }),
        invalidatesTags: ["employees"],
      }
    ),
    getAllOoo: builder.query<OOOModel[], void>({
      query: () => ({
        url: "/employees/list_ooo/",
      }),
      transformResponse(response: any) {
        return response.ooo_list;
      },
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
  useGetEmployeesQuery,
  useGetRolesQuery,
  useCreateEmployeeMutation,
  useGetAllOooQuery,
  useGetAllOooTypesQuery,
  useCreateOooMutation,
  useDeleteOooMutation,
} = employeesApi;
