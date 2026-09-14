import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoFactorRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function FactorsPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Factors" description="Factor exposures across the research universe." columns={['Factor', 'Symbol', 'Exposure', 'Weight']} rows={enabled ? demoFactorRows : []} liveText="Create or load factors from the backend to populate this workspace." />;
}

