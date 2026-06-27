import React from 'react';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <Navbar />
          <main className="p-6">{children}</main>
        </div>
      </div>
    </div>
  );
}

