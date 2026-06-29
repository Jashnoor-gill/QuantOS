import React, { useEffect, useMemo, useState } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  AreaChart,
  Area,
  BarChart,
  Bar,
} from 'recharts';

import { api } from '../services/api';

type KPI = {
  label: string;
  value: string;
  hint?: string;
};

type SeriesPoint = { name: string; value: number };

type AnalyticsSummary = {
  sharpe_ratio: number | null;
  sortino_ratio: number | null;
  cagr: number | null;
  annualized_volatility: number | null;
  maximum_drawdown: number | null;
  calmar_ratio: number | null;
  win_rate: number | null;
  profit_factor: number | null;
};

type AnalyticsPerformance = {
  equity_series: SeriesPoint[];
  drawdown_series: SeriesPoint[];
};

type AnalyticsRisk = {
  monthly_returns: SeriesPoint[];
};

const formatPct = (v: number, digits = 2) => `${(v * 100).toFixed(digits)}%`;
const formatNum = (v: number, digits = 2) => v.toFixed(digits);

export function AnalyticsPage() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [performance, setPerformance] = useState<AnalyticsPerformance | null>(null);
  const [risk, setRisk] = useState<AnalyticsRisk | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const run = async () => {
      setLoading(true);
      try {
        // TODO: Choose real backtest_id/portfolio_id once UI supports selection.
        const backtestId = 1;
        const [s, p, r] = await Promise.all([
          api.get<AnalyticsSummary>(`/analytics/summary?backtest_id=${backtestId}`).then((res) => res.data),
          api.get<AnalyticsPerformance>(`/analytics/performance?backtest_id=${backtestId}`).then((res) => res.data),
          api.get<AnalyticsRisk>(`/analytics/risk?backtest_id=${backtestId}`).then((res) => res.data),
        ]);
        setSummary(s);
        setPerformance(p);
        setRisk(r);

      } finally {
        setLoading(false);
      }
    };
    run();
  }, []);

  const kpis: KPI[] = useMemo(() => {
    const s = summary;
    return [
      { label: 'Sharpe Ratio', value: s?.sharpe_ratio != null ? formatNum(s.sharpe_ratio, 2) : '—', hint: 'Risk-adjusted return' },
      { label: 'Sortino Ratio', value: s?.sortino_ratio != null ? formatNum(s.sortino_ratio, 2) : '—', hint: 'Downside-risk adjusted' },
      { label: 'CAGR', value: s?.cagr != null ? formatPct(s.cagr, 2) : '—', hint: 'Compounded annual growth' },
      { label: 'Volatility', value: s?.annualized_volatility != null ? formatPct(s.annualized_volatility, 2) : '—', hint: 'Annualized volatility' },
      { label: 'Max Drawdown', value: s?.maximum_drawdown != null ? formatPct(s.maximum_drawdown, 2) : '—', hint: 'Worst peak-to-trough decline' },
      { label: 'Win Rate', value: s?.win_rate != null ? formatPct(s.win_rate, 1) : '—', hint: 'Winning trades / periods' },
    ];
  }, [summary]);

  const equitySeries = performance?.equity_series ?? [];
  const drawdownSeries = performance?.drawdown_series ?? [];
  const monthlyReturns = risk?.monthly_returns ?? [];

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Analytics</h1>
          <p className="mt-2 text-slate-300">Performance KPIs and drawdown visualization.</p>
        </div>
      </div>

      <section>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
          {kpis.map((k) => (
            <div key={k.label} className="rounded border border-slate-800 bg-slate-900/30 p-4">
              <div className="text-sm text-slate-300">{k.label}</div>
              <div className="mt-2 text-2xl font-semibold">{k.value}</div>
              {k.hint ? <div className="mt-1 text-xs text-slate-400">{k.hint}</div> : null}
            </div>
          ))}
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-2 text-sm text-slate-300">Equity Trend</div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={equitySeries} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                <YAxis tick={{ fill: '#cbd5e1' }} />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-2 text-sm text-slate-300">Monthly Returns</div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyReturns} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                <YAxis tick={{ fill: '#cbd5e1' }} tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`} />
                <Tooltip formatter={(v: any) => `${(Number(v) * 100).toFixed(2)}%`} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]} fill="#22c55e" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      <section className="rounded border border-slate-800 bg-slate-900/30 p-4">
        <div className="mb-2 text-sm text-slate-300">Drawdown Curve</div>
        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={drawdownSeries} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
              <YAxis
                tick={{ fill: '#cbd5e1' }}
                tickFormatter={(v: number) => `${(Number(v) * 100).toFixed(0)}%`}
              />
              <Tooltip formatter={(v: any) => `${(Number(v) * 100).toFixed(2)}%`} />
              <Area type="monotone" dataKey="value" stroke="#f97316" fill="rgba(249,115,22,0.18)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-3 text-xs text-slate-400">Drawdown series comes from backend.</div>
      </section>
    </div>
  );
}


