import apiClient from '../../client'
import type { Employee } from '../queries/get-employees'

const deleteEmployeeMutation = async (payload: string) => {
  const { data } = await apiClient.delete<Employee>('/employees/' + payload)
  return data
}

export default deleteEmployeeMutation
