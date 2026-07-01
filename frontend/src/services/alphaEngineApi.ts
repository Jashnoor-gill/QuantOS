import { api } from './api';

export interface AlphaResponse {
  id: number;
  name: string;
  description: string | null;
  expression: string;
  status: string;
  sharpe: number | null;
  turnover: number | null;
  fitness: number | null;
  created_at: string;
}

export interface AlphaListResponse {
  items: AlphaResponse[];
}

export const getAlphas = async (): Promise<AlphaListResponse> => {
  const response = await api.get('/alpha-engine/alphas');
  return response.data;
};
