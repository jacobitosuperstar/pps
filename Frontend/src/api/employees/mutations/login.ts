import apiClient from '../../client'

export interface LoginPayload {
  identification: string
  password: string
}

export interface LoginResponse {
  response: string
  employee: {
    identification: string
    names: string
    last_names: string
    role: string
    birthday: string
    date_joined: string
    last_login: string
  }
  token: string
}

export const loginMutation = async (payload: LoginPayload) => {
  const { data } = await apiClient.post<LoginResponse>(
    '/employees/login',
    payload
  )
  return data
}
