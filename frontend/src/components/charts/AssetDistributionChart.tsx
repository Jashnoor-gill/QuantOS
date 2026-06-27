import React from 'react';
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from 'recharts';

export type DistributionDatum = {
  name: string;
  value: number;
};

const COLORS = [
  '#4f46e5',
  '#22c55e',
  '#f97316',
  '#06b6d4',
  '#ef4444',
  '#a855f7',
  '#eab308',
  '#14b8a6',
];

export function AssetDistributionChart({
  data,
  loading,
  error,
}: {
  data?: DistributionDatum[];
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
        <PieChart>
          <Tooltip />
          <Legend />
          <Pie data={data ?? []} dataKey="value" nameKey="name" outerRadius={95}>
            {(data ?? []).map((_, idx) => (
              <Cell key={idx} fill={COLORS[idx % COLORS.length]} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

