import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoStrategyRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function StrategiesPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Strategies" description="Research strategies and their current operating status." columns={['Strategy', 'Type', 'Status', 'Return']} rows={enabled ? demoStrategyRows : []} liveText="Create or load strategies from the backend to populate this workspace." />;
}

