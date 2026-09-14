import type { Alpha, Backtest, FactorExposure, Portfolio, Strategy } from '../services/dashboardApi';

export const demoFactorExposures: FactorExposure[] = [
  { id: 1, factor_name: 'Momentum', symbol: 'NVDA', exposure: 1.42, weight: 0.18 },
  { id: 2, factor_name: 'Value', symbol: 'JPM', exposure: 0.86, weight: 0.14 },
  { id: 3, factor_name: 'Quality', symbol: 'MSFT', exposure: 1.12, weight: 0.16 },
  { id: 4, factor_name: 'Low Volatility', symbol: 'KO', exposure: 0.74, weight: 0.11 },
  { id: 5, factor_name: 'Momentum', symbol: 'AMD', exposure: 1.08, weight: 0.13 },
  { id: 6, factor_name: 'Size', symbol: 'IWM', exposure: 0.63, weight: 0.09 },
];

export const demoAlphas: Alpha[] = [
  { id: 101, status: 'active' }, { id: 102, status: 'active' }, { id: 103, status: 'draft' },
];
export const demoStrategies: Strategy[] = [
  { id: 201, strategy_type: 'Momentum', status: 'active' },
  { id: 202, strategy_type: 'Mean Reversion', status: 'active' },
  { id: 203, strategy_type: 'Factor Blend', status: 'paused' },
];
export const demoBacktests: Backtest[] = [
  { id: 301, status: 'completed', strategy_id: 201 },
  { id: 302, status: 'completed', strategy_id: 202 },
  { id: 303, status: 'running', strategy_id: 203 },
];
export const demoPortfolios: Portfolio[] = [
  { id: 401, status: 'active', strategy_id: 201 },
  { id: 402, status: 'active', strategy_id: 202 },
];

export const demoMarketRows = [
  ['NVDA', 'NVIDIA Corporation', '$138.85', '+2.84%', 'Momentum'],
  ['MSFT', 'Microsoft Corporation', '$510.92', '+1.16%', 'Quality'],
  ['JPM', 'JPMorgan Chase', '$291.37', '-0.42%', 'Value'],
  ['KO', 'Coca-Cola Company', '$68.44', '+0.31%', 'Low Volatility'],
];
export const demoFactorRows = demoFactorExposures.map((item) => [item.factor_name, item.symbol, item.exposure.toFixed(2), `${((item.weight ?? 0) * 100).toFixed(1)}%`]);
export const demoAlphaRows = [['Alpha Momentum 01', 'active', '1.68', '2026-06-14'], ['Quality Carry', 'active', '1.31', '2026-06-11'], ['Value Reversal', 'draft', '—', '2026-06-09']];
export const demoStrategyRows = [['Momentum Core', 'Momentum', 'active', '12.4%'], ['Reversion Plus', 'Mean Reversion', 'active', '9.7%'], ['Factor Blend', 'Factor Blend', 'paused', '6.2%']];
export const demoBacktestRows = [['BT-00301', 'Momentum Core', 'completed', '18.4%', '1.68'], ['BT-00302', 'Reversion Plus', 'completed', '12.1%', '1.31'], ['BT-00303', 'Factor Blend', 'running', '—', '—']];
export const demoPortfolioRows = [['Core Quant Portfolio', 'NVDA / MSFT / JPM', '14.8%', '1.42'], ['Defensive Tilt', 'KO / IWM / JPM', '8.6%', '0.94']];
export const demoRiskRows = [['Value at Risk (95%)', '−2.84%', 'Within limit'], ['Expected Shortfall', '−4.17%', 'Within limit'], ['Beta', '0.86', 'Balanced'], ['Max Drawdown', '−8.2%', 'Watch']];

export type DemoAnalytics = {
  summary: { sharpe_ratio: number; sortino_ratio: number; cagr: number; annualized_volatility: number; maximum_drawdown: number; calmar_ratio: number; win_rate: number; profit_factor: number };
  performance: { equity_series: { name: string; value: number }[]; drawdown_series: { name: string; value: number }[] };
  risk: { monthly_returns: { name: string; value: number }[] };
};

export const demoAnalytics: DemoAnalytics = {
  summary: { sharpe_ratio: 1.68, sortino_ratio: 2.44, cagr: 0.184, annualized_volatility: 0.137, maximum_drawdown: -0.082, calmar_ratio: 2.24, win_rate: 0.59, profit_factor: 1.74 },
  performance: { equity_series: [{ name: 'Jan', value: 100 }, { name: 'Feb', value: 106 }, { name: 'Mar', value: 112 }, { name: 'Apr', value: 109 }, { name: 'May', value: 121 }, { name: 'Jun', value: 128 }, { name: 'Jul', value: 136 }, { name: 'Aug', value: 142 }], drawdown_series: [{ name: 'Jan', value: 0 }, { name: 'Feb', value: -0.02 }, { name: 'Mar', value: -0.01 }, { name: 'Apr', value: -0.05 }, { name: 'May', value: -0.02 }, { name: 'Jun', value: -0.03 }, { name: 'Jul', value: -0.01 }, { name: 'Aug', value: -0.015 }] },
  risk: { monthly_returns: [{ name: 'Jan', value: 0.04 }, { name: 'Feb', value: 0.06 }, { name: 'Mar', value: 0.05 }, { name: 'Apr', value: -0.03 }, { name: 'May', value: 0.11 }, { name: 'Jun', value: 0.06 }, { name: 'Jul', value: 0.06 }, { name: 'Aug', value: 0.04 }] },
};