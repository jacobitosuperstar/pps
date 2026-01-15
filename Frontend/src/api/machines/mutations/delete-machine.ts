import apiClient from '../../client'
import type { Machine } from '../queries/get-machines'

const deleteMachineMutation = async (payload: string) => {
  const { data } = await apiClient.delete<Machine>('/machines/' + payload)
  return data
}

export default deleteMachineMutation
