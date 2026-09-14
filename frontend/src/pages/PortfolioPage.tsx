import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoPortfolioRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function PortfolioPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Portfolio" description="Model portfolios, allocation snapshots, and performance." columns={['Portfolio', 'Holdings', 'Return', 'Sharpe']} rows={enabled ? demoPortfolioRows : []} liveText="Sign in and load a portfolio to populate this workspace." />;
}

