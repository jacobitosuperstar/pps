import apiClient from '../../client'
import type { Employee } from '../queries/get-employees'

export interface CreateEmployeePayload {
  identification: string
  names: string
  last_names: string
  role: string
  birthday: string
  password: string
}

const createEmployeeMutation = async (payload: CreateEmployeePayload) => {
  const { data } = await apiClient.post<Employee>('/employees/', payload)
  return data
}

export default createEmployeeMutation
