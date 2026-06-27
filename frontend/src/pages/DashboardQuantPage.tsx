import React from 'react';

import { useQuery } from 'react-query';

import { DashboardCard } from '../components/DashboardCard';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { AssetDistributionChart } from '../components/charts/AssetDistributionChart';
import { StrategyCountChart } from '../components/charts/StrategyCountChart';
import { BacktestCountChart } from '../components/charts/BacktestCountChart';
import {
  fetchAlphas,
  fetchBacktests,
  fetchFactorExposures,
  fetchPortfolios,
  fetchStrategies,
} from '../services/dashboardApi';

import type { Alpha, Backtest, FactorExposure, Portfolio, Strategy } from '../services/dashboardApi';

function groupBy<T>(arr: T[], keyFn: (item: T) => string) {
  const m = new Map<string, number>();
  for (const item of arr) {
    const k = keyFn(item);
    m.set(k, (m.get(k) ?? 0) + 1);
  }
  return m;
}


export function DashboardQuantPage() {
  const factorExposuresQuery = useQuery<FactorExposure[], Error>(
    ['factorExposures'],
    fetchFactorExposures,
    { staleTime: 60_000 },
  );

  const alphasQuery = useQuery<Alpha[], Error>(['alphas'], fetchAlphas, {
    staleTime: 60_000,
  });

  const strategiesQuery = useQuery<Strategy[], Error>(
    ['strategies'],
    fetchStrategies,
    { staleTime: 60_000 },
  );

  const backtestsQuery = useQuery<Backtest[], Error>(
    ['backtests'],
    fetchBacktests,
    { staleTime: 60_000 },
  );

  const portfoliosQuery = useQuery<Portfolio[], Error>(
    ['portfolios'],
    fetchPortfolios,
    { staleTime: 60_000 },
  );

  const overallLoading =
    factorExposuresQuery.isLoading ||
    alphasQuery.isLoading ||
    strategiesQuery.isLoading ||
    backtestsQuery.isLoading ||
    portfoliosQuery.isLoading;

  const overallError =
    factorExposuresQuery.error ||
    alphasQuery.error ||
    strategiesQuery.error ||
    backtestsQuery.error ||
    portfoliosQuery.error;

  const assetDistributionData = React.useMemo(() => {
    const items = factorExposuresQuery.data ?? [];
    const bySymbol = groupBy(items, (x) => x.symbol);

    const asArray = Array.from(bySymbol.entries())
      .map(([name, count]) => ({ name, value: count }))
      .sort((a, b) => b.value - a.value)
      .slice(0, 8);

    return asArray;
  }, [factorExposuresQuery.data]);

  const strategyCountData = React.useMemo(() => {
    const items = strategiesQuery.data ?? [];
    const byType = groupBy(items, (s) => s.strategy_type);

    return Array.from(byType.entries())
      .map(([name, count]) => ({ name, value: count }))
      .sort((a, b) => b.value - a.value);
  }, [strategiesQuery.data]);

  const backtestCountData = React.useMemo(() => {
    const items = backtestsQuery.data ?? [];
    const byStatus = groupBy(items, (b) => b.status);

    return Array.from(byStatus.entries())
      .map(([name, count]) => ({ name, value: count }))
      .sort((a, b) => b.value - a.value);
  }, [backtestsQuery.data]);

  const totalAssets = (factorExposuresQuery.data ?? []).length;
  const totalFactors = new Set((factorExposuresQuery.data ?? []).map((x) => x.factor_name)).size;
  const totalAlphas = (alphasQuery.data ?? []).length;
  const totalStrategies = (strategiesQuery.data ?? []).length;
  const totalBacktests = (backtestsQuery.data ?? []).length;
  const totalPortfolios = (portfoliosQuery.data ?? []).length;

  if (overallLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold">Quant Dashboard</h1>
        <LoadingState label="Loading dashboard..." />
      </div>
    );
  }

  if (overallError) {
    return (
      <div className="space-y-6">
        <h1 className="text-2xl font-semibold">Quant Dashboard</h1>
        <ErrorState message={overallError.message} />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Quant Dashboard</h1>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
        <DashboardCard title="Total Assets" value={totalAssets} />
        <DashboardCard title="Total Factors" value={totalFactors} />
        <DashboardCard title="Total Alphas" value={totalAlphas} />
        <DashboardCard title="Total Strategies" value={totalStrategies} />
        <DashboardCard title="Total Backtests" value={totalBacktests} />
        <DashboardCard title="Total Portfolios" value={totalPortfolios} />
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <section className="space-y-2">
          <div className="text-sm text-slate-300">Asset distribution (top symbols)</div>
          <AssetDistributionChart
            data={assetDistributionData}
            loading={factorExposuresQuery.isLoading}
            error={!!factorExposuresQuery.error}
          />
        </section>

        <section className="space-y-2">
          <div className="text-sm text-slate-300">Strategy count (by strategy type)</div>
          <StrategyCountChart
            data={strategyCountData}
            loading={strategiesQuery.isLoading}
            error={!!strategiesQuery.error}
          />
        </section>

        <section className="space-y-2 lg:col-span-2">
          <div className="text-sm text-slate-300">Backtest count (by status)</div>
          <BacktestCountChart
            data={backtestCountData}
            loading={backtestsQuery.isLoading}
            error={!!backtestsQuery.error}
          />
        </section>
      </div>
    </div>
  );
}

