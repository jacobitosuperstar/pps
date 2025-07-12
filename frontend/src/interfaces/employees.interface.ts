export type GetRolesResponse = {
  label: string;
  value: string;
}[];
export interface Employee {
  id: number;
  identification: string;
  names: string;
  last_names: string;
  role: string;
  birthday: Date | null;
}

export interface GetEmployeesParams {
  search?: string;
  page?: number;
  page_size?: number;
}

export interface GetEmployeesResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Employee[];
}

export interface CreateEmployeeDTO {
  identification: string;
  names: string;
  last_names: string;
  role: string;
  birthday: string;
}

export interface UpdateEmployeeDTO {
  id: number;
  names: string;
  last_names: string;
  role: string;
  birthday: string;
}

export interface EmployeeOption {
  id: number;
  label: string;
}

export interface GetOptionsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: EmployeeOption[];
}
