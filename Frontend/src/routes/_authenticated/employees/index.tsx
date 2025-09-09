import z from 'zod'
import { createFileRoute } from '@tanstack/react-router'
import { Employees } from '@/features/employees'
import { roles } from '@/features/employees/data/data'

const employeesSearchSchema = z.object({
  limit: z.number().optional().catch(10),
  offset: z.number().optional().catch(0),
  // Facet filters
  role: z
    .enum(roles.map((r) => r.value))
    .optional()
    .catch(undefined),
  // Per-column text filter (example for username)
  identification: z.string().optional().catch(''),
  names: z.string().optional().catch(''),
  last_names: z.string().optional().catch(''),
  birthday: z.string().optional().catch(''),
})

export const Route = createFileRoute('/_authenticated/employees/')({
  validateSearch: employeesSearchSchema,
  component: Employees,
})
