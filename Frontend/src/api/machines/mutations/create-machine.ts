import apiClient from '../../client'
import type { Machine } from '../queries/get-machines'

export interface CreateMachinePayload {
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
}

const createMachineMutation = async (payload: CreateMachinePayload) => {
  const { data } = await apiClient.post<Machine>('/machines/', payload)
  return data
}

export default createMachineMutation
