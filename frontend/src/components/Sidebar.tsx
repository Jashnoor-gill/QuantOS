import React from 'react';
import { NavLink } from 'react-router-dom';

const items: Array<{ to: string; label: string }> = [
  { to: '/dashboard', label: 'Dashboard' },
  { to: '/market-data', label: 'Market Data' },
  { to: '/factors', label: 'Factors' },
  { to: '/alphas', label: 'Alphas' },
  { to: '/strategies', label: 'Strategies' },
  { to: '/backtests', label: 'Backtests' },
  { to: '/portfolio', label: 'Portfolio' },
  { to: '/risk', label: 'Risk' },
  { to: '/analytics', label: 'Analytics' },
  { to: '/alpha-lab', label: 'Alpha Lab' },
  { to: '/reports', label: 'Reports' },
];


export function Sidebar() {
  return (
    <aside className="w-56 border-r border-slate-800 bg-slate-900/40 p-4">
      <div className="mb-4 text-lg font-semibold">QuantOS</div>
      <nav className="flex flex-col gap-2">
        {items.map((it) => (
          <NavLink
            key={it.to}
            to={it.to}
            className={({ isActive }) =>
              isActive
                ? 'rounded bg-indigo-600 px-3 py-2 text-sm font-medium'
                : 'rounded px-3 py-2 text-sm hover:bg-slate-800'
            }
          >
            {it.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

