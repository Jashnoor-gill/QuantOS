import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from 'recharts';

export type SimpleCountDatum = {
  name: string;
  value: number;
};

export function StrategyCountChart({
  data,
  loading,
  error,
}: {
  data?: SimpleCountDatum[];
  loading?: boolean;
  error?: boolean;
}) {
  if (loading) {
    return <div className="text-sm text-slate-300">Loading chart...</div>;
  }
  if (error) {
    return <div className="text-sm text-rose-300">Failed to load chart.</div>;
  }

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data ?? []} margin={{ top: 10, right: 20, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{ fill: '#cbd5e1', fontSize: 12 }} />
          <YAxis tick={{ fill: '#cbd5e1' }} />
          <Tooltip />
          <Bar dataKey="value" fill="#4f46e5" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

