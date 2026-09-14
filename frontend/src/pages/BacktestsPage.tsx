import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoBacktestRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function BacktestsPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Backtests" description="Historical runs, returns, and risk-adjusted results." columns={['Run', 'Strategy', 'Status', 'Return', 'Sharpe']} rows={enabled ? demoBacktestRows : []} liveText="Run a strategy to populate backtest history." />;
}

