import apiClient from '../../client'
import type { Machine } from '../queries/get-machines'

export interface UpdateMachinePayload {
  machine_id: string
  machine_code: string
  name: string
  status: 'active'
  location: string
  description: string
  manufacturer: string
  model: string
  serial_number: string
  installation_date: string
}

const updateMachineMutation = async (payload: UpdateMachinePayload) => {
  const { machine_id, ...rest } = payload

  const { data } = await apiClient.post<Machine>(
    '/machines/' + machine_id,
    rest
  )
  return data
}

export default updateMachineMutation
