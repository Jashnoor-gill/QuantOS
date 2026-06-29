import React, { useMemo, useState } from 'react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

type ReportSummary = {
  id: string;
  name: string;
  createdAt: string;
  status: 'Completed' | 'Running' | 'Failed';
  notes?: string;
};

type ReportDetail = {
  id: string;
  description: string;
  metrics: Array<{ label: string; value: string }>;
  equity: Array<{ label: string; value: number }>;
};

// TODO: Replace mock data with backend reporting endpoints.
const mockReports: ReportSummary[] = [
  { id: 'rpt-001', name: 'Strategy A — Monthly Report', createdAt: '2026-05-15', status: 'Completed', notes: 'Stable performance' },
  { id: 'rpt-002', name: 'Strategy B — Stress Test', createdAt: '2026-05-22', status: 'Completed', notes: 'Higher drawdowns' },
  { id: 'rpt-003', name: 'Portfolio — Risk Attribution', createdAt: '2026-06-02', status: 'Running', notes: 'In progress' },
  { id: 'rpt-004', name: 'Alpha Scan — Selection', createdAt: '2026-06-10', status: 'Failed', notes: 'Data missing' },
];

const mockDetailById: Record<string, ReportDetail> = {
  'rpt-001': {
    id: 'rpt-001',
    description: 'Mock report details for Strategy A.',
    metrics: [
      { label: 'Sharpe', value: '1.41' },
      { label: 'Sortino', value: '2.02' },
      { label: 'CAGR', value: '16.3%' },
      { label: 'Max Drawdown', value: '-24.1%' },
      { label: 'Win Rate', value: '56.0%' },
    ],
    equity: [
      { label: 'Jan', value: 100 },
      { label: 'Feb', value: 112 },
      { label: 'Mar', value: 121 },
      { label: 'Apr', value: 116 },
      { label: 'May', value: 130 },
      { label: 'Jun', value: 126 },
    ],
  },
  'rpt-002': {
    id: 'rpt-002',
    description: 'Mock report details for Strategy B.',
    metrics: [
      { label: 'Sharpe', value: '0.98' },
      { label: 'Sortino', value: '1.32' },
      { label: 'CAGR', value: '9.4%' },
      { label: 'Max Drawdown', value: '-31.7%' },
      { label: 'Win Rate', value: '51.3%' },
    ],
    equity: [
      { label: 'Jan', value: 100 },
      { label: 'Feb', value: 107 },
      { label: 'Mar', value: 101 },
      { label: 'Apr', value: 95 },
      { label: 'May', value: 103 },
      { label: 'Jun', value: 98 },
    ],
  },
  'rpt-003': {
    id: 'rpt-003',
    description: 'Mock report details for Portfolio risk attribution.',
    metrics: [
      { label: 'Sharpe', value: '—' },
      { label: 'Sortino', value: '—' },
      { label: 'CAGR', value: '—' },
      { label: 'Max Drawdown', value: '—' },
      { label: 'Win Rate', value: '—' },
    ],
    equity: [
      { label: 'Jan', value: 100 },
      { label: 'Feb', value: 104 },
      { label: 'Mar', value: 106 },
      { label: 'Apr', value: 105 },
      { label: 'May', value: 108 },
      { label: 'Jun', value: 109 },
    ],
  },
  'rpt-004': {
    id: 'rpt-004',
    description: 'Mock report details for Alpha Scan (failed).',
    metrics: [
      { label: 'Sharpe', value: '—' },
      { label: 'Sortino', value: '—' },
      { label: 'CAGR', value: '—' },
      { label: 'Max Drawdown', value: '—' },
      { label: 'Win Rate', value: '—' },
    ],
    equity: [
      { label: 'Jan', value: 100 },
      { label: 'Feb', value: 99 },
      { label: 'Mar', value: 98 },
      { label: 'Apr', value: 98 },
      { label: 'May', value: 98 },
      { label: 'Jun', value: 98 },
    ],
  },
};

export function ReportsPage() {
  const [selectedId, setSelectedId] = useState<string>(mockReports[0]?.id ?? '');

  const selected = useMemo(() => mockDetailById[selectedId], [selectedId]);
  const selectedSummary = useMemo(
    () => mockReports.find((r) => r.id === selectedId),
    [selectedId]
  );

  const exportEnabled = selectedSummary?.status === 'Completed';

  return (
    <div className="space-y-6">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Reports</h1>
          <p className="mt-2 text-slate-300">Browse reports, inspect details, and export (placeholder).</p>
        </div>

        <button
          disabled={!exportEnabled}
          onClick={() => {
            // Placeholder: no fake API calls.
            alert(exportEnabled ? 'Export started (mock placeholder)' : 'Export only available for completed reports');
          }}
          className="rounded bg-indigo-600 px-4 py-2 text-sm font-medium hover:bg-indigo-500 disabled:opacity-60"
        >
          Export
        </button>
      </div>

      <section className="grid grid-cols-1 gap-4 xl:grid-cols-3">
        <div className="xl:col-span-1 rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-3 text-sm text-slate-300">Reports Table</div>

          <div className="overflow-auto">
            <table className="w-full text-left text-sm">
              <thead className="text-xs text-slate-400">
                <tr>
                  <th className="pb-2">Name</th>
                  <th className="pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {mockReports.map((r) => {
                  const isActive = r.id === selectedId;
                  const statusColor =
                    r.status === 'Completed' ? 'text-emerald-300' : r.status === 'Running' ? 'text-indigo-300' : 'text-rose-300';
                  return (
                    <tr
                      key={r.id}
                      onClick={() => setSelectedId(r.id)}
                      className={`cursor-pointer ${isActive ? 'bg-slate-800/60' : 'hover:bg-slate-800/30'}`}
                    >
                      <td className="py-2 pr-3">
                        <div className="font-medium">{r.name}</div>
                        <div className="text-xs text-slate-400">{r.createdAt}</div>
                      </td>
                      <td className={`py-2 ${statusColor}`}>{r.status}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        <div className="xl:col-span-2 rounded border border-slate-800 bg-slate-900/30 p-4">
          <div className="mb-3 flex items-start justify-between gap-4">
            <div>
              <div className="text-sm text-slate-300">Report Details View</div>
              <div className="mt-1 text-lg font-semibold">{selectedSummary?.name ?? 'Select a report'}</div>
              <div className="mt-1 text-xs text-slate-400">ID: {selectedSummary?.id ?? '—'}</div>
            </div>
            {selectedSummary?.notes ? <div className="max-w-xs text-xs text-slate-300">{selectedSummary.notes}</div> : null}
          </div>

          {!selected ? (
            <div className="text-sm text-slate-300">No report selected.</div>
          ) : (
            <div className="space-y-4">
              <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
                <div className="text-sm text-slate-300">Description</div>
                <div className="mt-2 text-slate-200">{selected.description}</div>
              </div>

              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
                {selected.metrics.map((m) => (
                  <div key={m.label} className="rounded border border-slate-800 bg-slate-900/30 p-3">
                    <div className="text-xs text-slate-400">{m.label}</div>
                    <div className="mt-1 text-lg font-semibold">{m.value}</div>
                  </div>
                ))}
              </div>

              <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
                <div className="mb-2 text-sm text-slate-300">Equity Preview (mock)</div>
                <div className="h-64 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={selected.equity} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="label" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
                      <YAxis tick={{ fill: '#cbd5e1' }} />
                      <Tooltip />
                      <Line type="monotone" dataKey="value" stroke="#6366f1" strokeWidth={2} dot={false} />
                    </LineChart>
                  </ResponsiveContainer>
                </div>

                <div className="mt-2 text-xs text-slate-400">
                  TODO: load real report plots (equity, drawdown, etc.) from backend.
                </div>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

