import React, { useMemo, useState } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, AreaChart, Area } from 'recharts';

type Metrics = {
  sharpe: number;
  sortino: number;
  maxDrawdown: number;
  winRate: number;
};

type Point = { label: string; value: number };

type DrawdownPoint = { label: string; dd: number };

// TODO: Replace editor + run logic with backend alpha evaluation once endpoints exist.
export function AlphaLabPage() {
  const [alphaText, setAlphaText] = useState(
    `# Example Alpha (mock)\n\nalpha = rank(close) - rank(open)\n# Replace with your DSL / expression\n`
  );
  const [running, setRunning] = useState(false);
  const [lastRunAt, setLastRunAt] = useState<string | null>(null);

  const mockResult = useMemo(() => {
    const equity: Point[] = [
      { label: 'W1', value: 100 },
      { label: 'W2', value: 108 },
      { label: 'W3', value: 105 },
      { label: 'W4', value: 113 },
      { label: 'W5', value: 122 },
      { label: 'W6', value: 118 },
      { label: 'W7', value: 127 },
      { label: 'W8', value: 134 },
      { label: 'W9', value: 129 },
      { label: 'W10', value: 141 },
      { label: 'W11', value: 149 },
      { label: 'W12', value: 156 },
    ];

    const dd: DrawdownPoint[] = [
      { label: 'W1', dd: 0.0 },
      { label: 'W2', dd: -0.01 },
      { label: 'W3', dd: -0.04 },
      { label: 'W4', dd: -0.02 },
      { label: 'W5', dd: -0.01 },
      { label: 'W6', dd: -0.03 },
      { label: 'W7', dd: -0.02 },
      { label: 'W8', dd: -0.01 },
      { label: 'W9', dd: -0.05 },
      { label: 'W10', dd: -0.02 },
      { label: 'W11', dd: -0.01 },
      { label: 'W12', dd: -0.015 },
    ];

    const metrics: Metrics = {
      sharpe: 1.68,
      sortino: 2.44,
      maxDrawdown: -0.05,
      winRate: 0.59,
    };

    return { equity, dd, metrics };
  }, []);

  const handleRun = async () => {
    setRunning(true);

    // Mock delay to simulate async backend evaluation.
    await new Promise((r) => setTimeout(r, 700));

    setLastRunAt(new Date().toLocaleString());
    setRunning(false);
  };

  const metrics = mockResult.metrics;

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Alpha Lab</h1>
          <p className="mt-2 text-slate-300">Edit an alpha, run it, and inspect mock results.</p>
        </div>
        <div className="text-xs text-slate-400">
          {lastRunAt ? <div>Last run: {lastRunAt}</div> : <div>Not run yet</div>}
        </div>
      </div>

      <section className="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <div className="rounded border border-slate-800 bg-slate-900/30 p-4 xl:col-span-2">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div className="text-sm text-slate-300">Alpha Editor (Monaco placeholder)</div>
            <button
              onClick={handleRun}
              disabled={running}
              className="rounded bg-indigo-600 px-4 py-2 text-sm font-medium hover:bg-indigo-500 disabled:opacity-60"
            >
              {running ? 'Running…' : 'Run Alpha'}
            </button>
          </div>

          {/*
            TODO: Replace textarea with Monaco editor when monaco-editor is installed.
          */}
          <textarea
            value={alphaText}
            onChange={(e) => setAlphaText(e.target.value)}
            className="h-72 w-full resize-none rounded border border-slate-800 bg-slate-950/40 p-3 font-mono text-sm text-slate-100 outline-none"
            spellCheck={false}
          />

          <div className="mt-2 text-xs text-slate-400">
            TODO: submit alpha to backend endpoint and load equity/drawdown results.
          </div>
        </div>

        <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-3 text-sm text-slate-300">Metrics Panel</div>

          <div className="grid grid-cols-1 gap-3">
            <div className="rounded border border-slate-800 bg-slate-900/30 p-3">
              <div className="text-xs text-slate-400">Sharpe Ratio</div>
              <div className="mt-1 text-lg font-semibold">{metrics.sharpe.toFixed(2)}</div>
            </div>
            <div className="rounded border border-slate-800 bg-slate-900/30 p-3">
              <div className="text-xs text-slate-400">Sortino Ratio</div>
              <div className="mt-1 text-lg font-semibold">{metrics.sortino.toFixed(2)}</div>
            </div>
            <div className="rounded border border-slate-800 bg-slate-900/30 p-3">
              <div className="text-xs text-slate-400">Max Drawdown</div>
              <div className="mt-1 text-lg font-semibold">{(metrics.maxDrawdown * 100).toFixed(2)}%</div>
            </div>
            <div className="rounded border border-slate-800 bg-slate-900/30 p-3">
              <div className="text-xs text-slate-400">Win Rate</div>
              <div className="mt-1 text-lg font-semibold">{(metrics.winRate * 100).toFixed(1)}%</div>
            </div>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 xl:grid-cols-2">
        <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-2 text-sm text-slate-300">Equity Curve (mock)</div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockResult.equity} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                <YAxis tick={{ fill: '#cbd5e1' }} />
                <Tooltip />
                <Line type="monotone" dataKey="value" stroke="#22c55e" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-2 text-sm text-slate-300">Drawdown (mock)</div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockResult.dd} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                <YAxis tick={{ fill: '#cbd5e1' }} tickFormatter={(v) => `${(Number(v) * 100).toFixed(0)}%`} />
                <Tooltip formatter={(v: any) => `${(Number(v) * 100).toFixed(2)}%`} />
                <Area type="monotone" dataKey="dd" stroke="#f97316" fill="rgba(249,115,22,0.18)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>
    </div>
  );
}

