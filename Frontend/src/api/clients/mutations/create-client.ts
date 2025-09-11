import apiClient from '../../client'
import type { Client } from '../queries/get-clients'

export interface CreateClientPayload {
  client_id: string
  client_name: string
  client_email: string
  client_phone_code: string
  client_phone_number: string
}

const createClientMutation = async (payload: CreateClientPayload) => {
  const { data } = await apiClient.post<Client>('/clients/', payload)
  return data
}

export default createClientMutation
