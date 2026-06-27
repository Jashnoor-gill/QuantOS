import React from 'react';

type DashboardCardProps = {
  title: string;
  value?: React.ReactNode;
  loading?: boolean;
  error?: boolean;
};

export function DashboardCard({ title, value, loading, error }: DashboardCardProps) {
  return (
    <div className="rounded border border-slate-800 bg-slate-900/30 p-4">
      <div className="text-sm text-slate-300">{title}</div>
      <div className="mt-2 text-2xl font-semibold">
        {loading ? (
          <div className="h-7 w-24 animate-pulse rounded bg-slate-800" />
        ) : error ? (
          <span className="text-rose-400">Error</span>
        ) : (
          value ?? '—'
        )}
      </div>
    </div>
  );
}

