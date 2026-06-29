import React from 'react';
import { Sidebar } from './Sidebar';
import { Navbar } from './Navbar';
import { ErrorBoundary } from './ErrorBoundary';
import { ToastProvider } from './toast/ToastProvider';

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <ToastProvider>
      <ErrorBoundary>
        <div className="min-h-screen bg-terminal-bg text-terminal-fg">
          <div className="flex">
            <Sidebar />
            <div className="flex-1">
              <Navbar />
              <main className="p-6">{children}</main>
            </div>
          </div>
        </div>
      </ErrorBoundary>
    </ToastProvider>
  );
}




