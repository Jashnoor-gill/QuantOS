import React from 'react';
import { useDemoMode } from '../demo/DemoProvider';

type DemoPageProps = { title: string; description: string; columns: string[]; rows: string[][]; liveText: string };

export function DemoPage({ title, description, columns, rows, liveText }: DemoPageProps) {
  const { enabled } = useDemoMode();
  return (
    <div className="space-y-6">
      <div><h1 className="text-2xl font-semibold">{title}</h1><p className="mt-2 text-slate-300">{description}</p></div>
      {enabled ? (
        <div className="overflow-hidden rounded border border-slate-800 bg-slate-900/40 shadow-xl shadow-black/10">
          <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3"><span className="text-sm text-slate-300">Demo dataset</span><span className="rounded-full bg-emerald-400/10 px-2 py-1 text-xs text-emerald-300">LIVE PREVIEW</span></div>
          <div className="overflow-auto"><table className="w-full min-w-[620px] text-left text-sm"><thead className="bg-slate-950/40 text-xs uppercase tracking-wide text-slate-400"><tr>{columns.map((column) => <th key={column} className="px-4 py-3">{column}</th>)}</tr></thead><tbody>{rows.map((row, index) => <tr key={`${row[0]}-${index}`} className="border-t border-slate-800/80 hover:bg-slate-800/30">{row.map((cell, cellIndex) => <td key={`${cell}-${cellIndex}`} className={`px-4 py-3 ${cellIndex === 0 ? 'font-medium text-slate-100' : 'text-slate-300'}`}>{cell}</td>)}</tr>)}</tbody></table></div>
        </div>
      ) : <div className="rounded border border-dashed border-slate-700 bg-slate-900/20 p-8 text-sm text-slate-400">{liveText}</div>}
    </div>
  );
}