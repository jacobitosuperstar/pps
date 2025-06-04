import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { objectToFormData } from "@/helper/object-to-formdata";
import type { MachineType } from "@/interfaces/machine";

export const machinesApi = createApi({
  reducerPath: "machinesApi",
  baseQuery: appBaseQuery,
  tagTypes: ["machine-type"],
  endpoints: (builder) => ({
    getExistingMachinesTypes: builder.query<string[], void>({
      query: () => ({
        url: "/machines/existing_machine_types/",
        method: "get",
      }),
    }),
    getMachinesTypes: builder.query<MachineType[], void>({
      query: () => ({
        url: "/machines/list_machine_types/",
        method: "get",
      }),
    }),
    createMachineType: builder.mutation<string, MachineType>({
      query: (body) => ({
        url: "/machines/create_machine_type/",
        method: "POST",
        body: objectToFormData(body),
      }),
    }),
  }),
});

export const {
  useGetMachinesTypesQuery,
  useGetExistingMachinesTypesQuery,
  useCreateMachineTypeMutation,
} = machinesApi;
