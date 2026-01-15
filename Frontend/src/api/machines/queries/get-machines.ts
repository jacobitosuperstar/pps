import apiClient from '../../client'

export interface Machine {
  machine_code: string
  name: string
  machine_type: string
  status: 'active'
  location: string
  description: string
  manufacturer: string
  model: string
  serial_number: string
  installation_date: string
  last_maintenance: string
  next_maintenance: string
  id: number
  created_at: string
  updated_at: string
  deleted: boolean
  operators: []
  maintenance_records: []
}

export interface ClientFilters {
  machine_code?: string
  name?: string
  location?: string
  model?: string
  limit?: number // default 100, max 1000
  offset?: number // default 0
}

export interface GetMachinesResponse {
  results: Machine[]
  total_count: number
}

const getMachinesQuery = async (filters: ClientFilters = {}) => {
  const { data } = await apiClient.get<GetMachinesResponse>('/machines/', {
    params: filters,
  })
  return data
}

export default getMachinesQuery
