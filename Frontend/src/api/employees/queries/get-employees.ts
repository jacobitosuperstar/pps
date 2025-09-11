import apiClient from '../../client'

export interface Employee {
  identification: string
  names: string
  last_names: string
  role: string
  birthday: string
  date_joined: string
  last_login: string
}

export interface EmployeeFilters {
  identification?: string
  names?: string
  last_names?: string
  role?: string
  birthday?: string
  created_at_from?: string
  created_at_to?: string
  updated_at_from?: string
  updated_at_to?: string
  limit?: number // default 100, max 1000
  offset?: number // default 0
}

export interface GetEmployeesResponse {
  results: Employee[]
  total_count: number
}

const getEmployeesQuery = async (filters: EmployeeFilters = {}) => {
  const { data } = await apiClient.get<GetEmployeesResponse>('/employees/', {
    params: filters,
  })
  return data
}

export default getEmployeesQuery
