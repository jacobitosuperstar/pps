import apiClient from '../../client'

export interface Client {
  client_id: string
  client_name: string
  client_email: string
  client_phone_code: string
  client_phone_number: string
  created_at: string
  updated_at: string
  deleted: boolean
}

export interface ClientFilters {
  client_name?: string
  client_email?: string
  client_phone_code?: string
  client_phone_number?: string
  limit?: number // default 100, max 1000
  offset?: number // default 0
}

export interface GetClientsResponse {
  results: Client[]
  total_count: number
}

const getClientsQuery = async (filters: ClientFilters = {}) => {
  const { data } = await apiClient.get<GetClientsResponse>('/clients/', {
    params: filters,
  })
  return data
}

export default getClientsQuery
