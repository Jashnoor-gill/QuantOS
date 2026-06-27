import React from 'react';

export function ErrorState({ message }: { message?: string }) {
  return (
    <div className="rounded border border-rose-900/60 bg-rose-950/20 p-3">
      <div className="text-sm font-medium text-rose-300">Error</div>
      <div className="mt-1 text-sm text-slate-300">{message ?? 'Something went wrong.'}</div>
    </div>
  );
}

