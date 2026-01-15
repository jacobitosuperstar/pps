import z from 'zod'
import { createFileRoute } from '@tanstack/react-router'
import { Machines } from '@/features/machines'

const machinesSearchSchema = z.object({
  limit: z.number().optional().catch(10),
  offset: z.number().optional().catch(0),
  // Per-column text filter (example for username)
  machine_code: z.string().optional().catch(''),
  name: z.string().optional().catch(''),
  location: z.string().optional().catch(''),
  model: z.string().optional().catch(''),
})

export const Route = createFileRoute('/_authenticated/machines/')({
  validateSearch: machinesSearchSchema,
  component: Machines,
})
