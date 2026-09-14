import React from 'react';
import { DemoPage } from '../components/DemoPage';
import { demoMarketRows } from '../demo/demoData';
import { useDemoMode } from '../demo/DemoProvider';

export function MarketDataPage() {
  const { enabled } = useDemoMode();
  return <DemoPage title="Market Data" description="Market data ingestion and datasets." columns={['Symbol', 'Company', 'Last price', 'Today', 'Primary signal']} rows={enabled ? demoMarketRows : []} liveText="Connect a market data source to populate this workspace." />;
}

