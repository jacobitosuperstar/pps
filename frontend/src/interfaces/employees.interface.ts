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
  birthday: string | null;
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

export interface CreateEmployeeDto {
  identification: string;
  names: string;
  last_names: string;
  role: string;
  birthday: string;
}

export interface UpdateEmployeeDto {
  id: number;
  names: string;
  last_names: string;
  role: string;
  birthday: string;
}

// OOO
export interface OOOTypesResponse {
  non_paid_leave: "Vacaciones no pagas";
  non_paid_permit: "permiso no pago";
  non_work_accident: "Accidente no relacionado con el trabajo";
  paid_leave: "Vacaciones pagas";
  paid_permit: "permiso pago";
  work_accident: "Accidente de trabajo";
}

export interface OOOModel {
  id: number;
  created_at: string;
  updated_at: string;
  is_deleted: boolean;
  employee: Employee;
  ooo_type: string;
  start_date: string;
  end_date: string;
  description: string;
}

export interface CreateOooDto {
  employee_identification: number;
  ooo_type: string;
  start_date: string;
  end_date: string;
  description: string;
}

export interface CreateOooResponse {
  ooo_time: string;
}

export interface OOOType {
  id: keyof OOOTypesResponse;
  label: string;
}
