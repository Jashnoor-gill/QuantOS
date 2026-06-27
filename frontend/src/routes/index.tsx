import React from 'react';
import { DashboardPage } from '../pages/DashboardPage';
import { MarketDataPage } from '../pages/MarketDataPage';
import { FactorsPage } from '../pages/FactorsPage';
import { AlphasPage } from '../pages/AlphasPage';
import { StrategiesPage } from '../pages/StrategiesPage';
import { BacktestsPage } from '../pages/BacktestsPage';
import { PortfolioPage } from '../pages/PortfolioPage';
import { RiskPage } from '../pages/RiskPage';


export const IndexRoutes: Array<{ path: string; element: React.ReactNode }> = [
  { path: '/dashboard', element: <DashboardPage /> },
  { path: '/market-data', element: <MarketDataPage /> },
  { path: '/factors', element: <FactorsPage /> },
  { path: '/alphas', element: <AlphasPage /> },
  { path: '/strategies', element: <StrategiesPage /> },
  { path: '/backtests', element: <BacktestsPage /> },
  { path: '/portfolio', element: <PortfolioPage /> },
  { path: '/risk', element: <RiskPage /> },
];

