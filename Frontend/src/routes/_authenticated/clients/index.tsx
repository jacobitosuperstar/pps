import z from 'zod'
import { createFileRoute } from '@tanstack/react-router'
import { Clients } from '@/features/clients'

const clientsSearchSchema = z.object({
  limit: z.number().optional().catch(10),
  offset: z.number().optional().catch(0),
  // Per-column text filter (example for username)
  client_name: z.string().optional().catch(''),
  client_email: z.string().optional().catch(''),
  client_phone_code: z.string().optional().catch(''),
  client_phone_number: z.string().optional().catch(''),
})

export const Route = createFileRoute('/_authenticated/clients/')({
  validateSearch: clientsSearchSchema,
  component: Clients,
})
