export interface LoginDto {
  identification: string;
  password: string;
}

export interface LoginResponse {
  response: string;
}

export interface PinResponse {
  now: string;
}
