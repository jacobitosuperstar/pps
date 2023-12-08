import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { objectToFormData } from "@/helper/object-to-formdata";
import {
  CreateEmployeeDto,
  CreateEmployeeResponse,
  Employee,
  Roles,
} from "@/interfaces/employees.interface";

export const employeesApi = createApi({
  reducerPath: "employeesApi",
  baseQuery: appBaseQuery,
  endpoints: (builder) => ({
    getRoles: builder.query<Roles, void>({
      query: () => "/employees/roles/",
    }),
    getEmployees: builder.query<Employee[], void>({
      query: () => ({
        url: "/employees/",
      }),
    }),
    createEmployee: builder.mutation<CreateEmployeeResponse, CreateEmployeeDto>(
      {
        query: (body) => ({
          url: "/employees/create/",
          method: "POST",
          body: objectToFormData(body),
        }),
      }
    ),
  }),
});

export const {
  useGetEmployeesQuery,
  useGetRolesQuery,
  useCreateEmployeeMutation,
} = employeesApi;
