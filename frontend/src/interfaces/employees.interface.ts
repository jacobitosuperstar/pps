export interface RolesObject {
  accounting: string;
  hr: string;
  management: string;
  prod: string;
  prod_manager: string;
  quality: string;
}

export interface Role {
  id: keyof RolesObject;
  name: string;
}
export interface Employee {
  birthday: string | null;
  created_at: string;
  date_joined: string;
  identification: string;
  is_deleted: false;
  last_login: string;
  last_names: string;
  names: string;
  role: keyof RolesObject;
  updated_at: string;
}

export interface CreateEmployeeDto {
  identification: string;
  names: string;
  last_names: string;
  birthday: string;
  role: string;
}

export interface CreateEmployeeResponse {
  identification: string;
  role: string;
  generated_password: string | undefined;
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
