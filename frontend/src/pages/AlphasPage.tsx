import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoAlphaRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function AlphasPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Alphas" description="Signals ranked by quality, status, and recent research date." columns={['Name', 'Status', 'Sharpe', 'Updated']} rows={enabled ? demoAlphaRows : []} liveText="Create or load alpha signals from the backend to populate this workspace." />;
}

