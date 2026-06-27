import { api } from './api';

export type FactorExposure = {
  id: number;
  factor_name: string;
  symbol: string;
  exposure: number;
  weight?: number | null;
};

export type Alpha = { id: number; status: string };
export type Strategy = { id: number; strategy_type: string; status: string };
export type Backtest = { id: number; status: string; strategy_id: number };
export type Portfolio = { id: number; status: string; strategy_id: number };

export type ListResponse<T> = { items: T[] };

export async function fetchFactorExposures(): Promise<FactorExposure[]> {
  const res = await api.get<ListResponse<FactorExposure>>('/factor-engine/exposures', {
    params: { limit: 10000 },
  });
  return res.data.items;
}

export async function fetchAlphas(): Promise<Alpha[]> {
  const res = await api.get<ListResponse<Alpha>>('/alpha-engine/alphas', {
    params: { limit: 10000 },
  });
  return res.data.items;
}

export async function fetchStrategies(): Promise<Strategy[]> {
  const res = await api.get<ListResponse<Strategy>>('/strategy-engine/strategies', {
    params: { limit: 10000 },
  });
  return res.data.items;
}

export async function fetchBacktests(): Promise<Backtest[]> {
  const res = await api.get<ListResponse<Backtest>>('/backtesting-engine/backtests', {
    params: { limit: 10000 },
  });
  return res.data.items;
}

export async function fetchPortfolios(): Promise<Portfolio[]> {
  const res = await api.get<ListResponse<Portfolio>>('/portfolio-optimizer/portfolios', {
    params: { limit: 10000 },
  });
  return res.data.items;
}

