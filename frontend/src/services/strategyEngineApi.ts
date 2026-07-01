import { api } from './api';

export interface StrategyResponse {
  id: number;
  name: string;
  description: string | null;
  strategy_type: string;
  alpha_id: number;
  rebalance_frequency: number | null;
  status: string;
  created_at: string;
}

export interface StrategyListResponse {
  items: StrategyResponse[];
}

export const getStrategies = async (): Promise<StrategyListResponse> => {
  const response = await api.get('/strategy-engine/strategies');
  return response.data;
};
