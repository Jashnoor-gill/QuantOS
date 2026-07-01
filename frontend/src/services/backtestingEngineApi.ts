import { api } from './api';

export interface BacktestResponse {
  id: number;
  strategy_id: number;
  start_date: string;
  end_date: string;
  initial_capital: number;
  final_capital: number;
  total_return: number | null;
  sharpe_ratio: number | null;
  max_drawdown: number | null;
  status: string;
  created_at: string;
}

export interface BacktestListResponse {
  items: BacktestResponse[];
}

export const getBacktests = async (): Promise<BacktestListResponse> => {
  const response = await api.get('/backtesting-engine/backtests');
  return response.data;
};
