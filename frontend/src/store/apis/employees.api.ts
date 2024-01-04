import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { objectToFormData } from "@/helper/object-to-formdata";
import {
  CreateEmployeeDto,
  CreateEmployeeResponse,
  Employee,
  Role,
  RolesObject,
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
          url: "/employees/create/",
          method: "POST",
          body: objectToFormData(body),
        }),
        invalidatesTags: ["employees"],
      }
    ),
    getAllOoo: builder.query<Employee[], void>({
      query: () => ({
        url: "/employees/list_ooo/",
      }),
      transformResponse(response: any) {
        console.log(response);
        return response;
      },
      providesTags: ["ooo"],
    }),
  }),
});

export const {
  useGetEmployeesQuery,
  useGetRolesQuery,
  useCreateEmployeeMutation,
  useGetAllOooQuery,
} = employeesApi;
