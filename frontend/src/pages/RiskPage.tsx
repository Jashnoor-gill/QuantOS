import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoRiskRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function RiskPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Risk" description="Portfolio risk limits and monitoring signals." columns={['Metric', 'Value', 'Assessment']} rows={enabled ? demoRiskRows : []} liveText="Load a portfolio to calculate live risk metrics." />;
}

