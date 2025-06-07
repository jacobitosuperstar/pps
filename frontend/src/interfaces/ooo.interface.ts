export type OOOTypesResponse = { label: string; value: string }[];

export interface OOO {
  id: number;
  employee: number;
  ooo_type: string;
  start_date: string;
  end_date: string;
  description: string;
}

export interface GetOOOParams {
  search?: string;
  page?: number;
  page_size?: number;
}

export interface GetOOOResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: OOO[];
}

export interface CreateOOODTO {
  employee: number;
  ooo_type: string;
  start_date: string;
  end_date: string;
  description: string;
}

export interface UpdateOOODTO {
  id: number;
  ooo_type: string;
  start_date: string;
  end_date: string;
  description: string;
}
