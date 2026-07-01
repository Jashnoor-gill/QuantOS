import { api } from './api';

export interface RiskMetricResponse {
  id: number;
  portfolio_id: number;
  var_95: number | null;
  var_99: number | null;
  expected_shortfall: number | null;
  beta: number | null;
  volatility: number | null;
  max_drawdown: number | null;
  risk_score: number | null;
  created_at: string;
}

export interface RiskMetricListResponse {
  items: RiskMetricResponse[];
}

export const getRiskMetrics = async (): Promise<RiskMetricListResponse> => {
  const response = await api.get('/risk-engine/risk-metrics');
  return response.data;
};
