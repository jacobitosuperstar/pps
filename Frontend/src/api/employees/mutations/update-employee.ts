import apiClient from '../../client'
import type { Employee } from '../queries/get-employees'

export interface UpdateEmployeePayload {
  identification: string
  names: string
  last_names: string
  role: string
  birthday: string
  password: string
}

const updateEmployeeMutation = async (payload: UpdateEmployeePayload) => {
  const { identification, ...rest } = payload

  const { data } = await apiClient.put<Employee>(
    '/employees/' + identification,
    rest
  )
  return data
}

export default updateEmployeeMutation
