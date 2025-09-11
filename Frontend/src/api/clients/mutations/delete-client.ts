import apiClient from '../../client'
import type { Client } from '../queries/get-clients'

const deleteClientMutation = async (payload: string) => {
  const { data } = await apiClient.delete<Client>('/clients/' + payload)
  return data
}

export default deleteClientMutation
