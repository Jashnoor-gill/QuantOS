import React from 'react';
import { useAuth } from '../context/AuthContext';

export function Navbar() {
  const { user } = useAuth();

  return (
    <header className="flex items-center justify-between border-b border-slate-800 bg-slate-900/40 px-6 py-3">
      <div className="text-sm text-slate-300">{user ? `@${user}` : 'System'}</div>
      <div className="text-sm text-slate-300">QuantOS Dashboard</div>
    </header>
  );
}


