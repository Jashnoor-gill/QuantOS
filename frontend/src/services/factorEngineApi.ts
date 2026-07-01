import { api } from './api';

export interface FactorExposure {
  id: number;
  factor_name: string;
  symbol: string;
  exposure: number;
  weight: number | null;
  created_at: string;
  updated_at: string;
}

export interface FactorExposureListResponse {
  items: FactorExposure[];
}

export const getFactorExposures = async (): Promise<FactorExposureListResponse> => {
  const response = await api.get('/factor-engine/exposures');
  return response.data;
};
