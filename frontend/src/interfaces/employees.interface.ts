export interface Roles {
  accounting: string;
  hr: string;
  management: string;
  prod: string;
  prod_manager: string;
  quality: string;
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
  role: keyof Roles;
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
