import { api } from './api';

export interface AssetReturn {
  asset_id: string;
  returns: number[];
}

export interface OptimizeRequest {
  returns: AssetReturn[];
  target_return?: number;
  risk_aversion?: number;
}

export interface OptimizeResponse {
  weights: Record<string, number>;
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
}

export interface EfficientFrontierPoint {
  return_val: number;
  volatility: number;
  sharpe_ratio: number;
}

export interface EfficientFrontierResponse {
  points: EfficientFrontierPoint[];
}

export async function runMeanVarianceOptimization(
  payload: OptimizeRequest
): Promise<OptimizeResponse> {
  const res = await api.post<OptimizeResponse>(
    '/portfolio-optimizer/optimize/mean-variance',
    payload
  );
  return res.data;
}

export async function runMinVariancePortfolio(
  payload: OptimizeRequest
): Promise<OptimizeResponse> {
  const res = await api.post<OptimizeResponse>(
    '/portfolio-optimizer/optimize/min-variance',
    payload
  );
  return res.data;
}

export async function runRiskParityPortfolio(
  payload: OptimizeRequest
): Promise<OptimizeResponse> {
  const res = await api.post<OptimizeResponse>(
    '/portfolio-optimizer/optimize/risk-parity',
    payload
  );
  return res.data;
}

export async function fetchEfficientFrontier(
  payload: OptimizeRequest
): Promise<EfficientFrontierResponse> {
  const res = await api.post<EfficientFrontierResponse>(
    '/portfolio-optimizer/efficient-frontier',
    payload
  );
  return res.data;
}
