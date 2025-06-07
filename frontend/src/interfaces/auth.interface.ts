export interface LoginDTO {
  identification: string;
  password: string;
}

export interface LoginResponse {
  response: string;
  employee: {
    identification: string;
    names: string;
    last_names: string;
    role: string;
    birthday: string | null;
  };
  token: string;
}
