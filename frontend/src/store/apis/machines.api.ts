import { createApi } from "@reduxjs/toolkit/query/react";
import { appBaseQuery } from "./basequery";
import { objectToFormData } from "@/helper/object-to-formdata";
import { MachineType, MachineTypeKeys } from "@/interfaces/machine";

export const machinesApi = createApi({
  reducerPath: "machinesApi",
  baseQuery: appBaseQuery,
  tagTypes: ["machine-type"],
  endpoints: (builder) => ({
    getExistingMachinesTypes: builder.query<any, void>({
      query: (body) => ({
        url: "/machines/existing_machine_types/",
        method: "get",
      }),
      transformResponse(response: MachineTypeKeys) {
        if (!response) return [];

        return Object.keys(response).map((x) => {
          const key = x as keyof MachineTypeKeys;
          return {
            id: key,
            name: response[key] as string,
          };
        });
      },
    }),
    getMachinesTypes: builder.query<MachineType[], void>({
      query: () => ({
        url: "/machines/list_machine_types/",
        method: "get",
      }),
    }),
    createMachineType: builder.mutation<any, MachineType>({
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
