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

export interface AlphaCreate {
  name: string;
  description: string;
  expression: string;
  status: string;
}

export const createAlpha = async (alpha: AlphaCreate): Promise<AlphaResponse> => {
  const response = await api.post('/alpha-engine/alphas', alpha);
  return response.data;
};
