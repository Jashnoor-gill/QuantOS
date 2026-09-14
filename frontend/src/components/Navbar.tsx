import React from 'react';
import { useDemoMode } from '../demo/DemoProvider';

export function Navbar() {
  const { enabled, toggle } = useDemoMode();

  return (
    <header className="flex items-center justify-between border-b border-slate-800 bg-slate-900/40 px-6 py-3">
      <div className="text-sm text-slate-300">System</div>
      <div className="flex items-center gap-4">
        <label className="flex cursor-pointer items-center gap-2 text-xs text-slate-300">
          <input type="checkbox" checked={enabled} onChange={toggle} className="h-4 w-4 accent-emerald-400" />
          Demo mode
        </label>
        <div className="text-sm text-slate-300">QuantOS Dashboard</div>
      </div>
    </header>
  );
}

