import apiClient from '../../client'
import type { Client } from '../queries/get-clients'

export interface UpdateClientPayload {
  client_id: string
  client_name: string
  client_email: string
  client_phone_code: string
  client_phone_number: string
}

const updateClientMutation = async (payload: UpdateClientPayload) => {
  const { client_id, ...rest } = payload

  const { data } = await apiClient.post<Client>('/clients/' + client_id, rest)
  return data
}

export default updateClientMutation
