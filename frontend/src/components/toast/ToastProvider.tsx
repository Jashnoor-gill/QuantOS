import React from 'react';

export type ToastTone = 'success' | 'error' | 'info';

export type Toast = {
  id: string;
  title: string;
  message?: string;
  tone: ToastTone;
  createdAt: number;
  ttlMs?: number;
};

type Ctx = {
  pushToast: (t: Omit<Toast, 'id' | 'createdAt'>) => void;
};

const ToastContext = React.createContext<Ctx | null>(null);

function toneStyles(tone: ToastTone) {
  switch (tone) {
    case 'success':
      return {
        ring: 'ring-emerald-500/30',
        bg: 'bg-emerald-950/20',
        text: 'text-emerald-200',
        border: 'border-emerald-900/60',
      };
    case 'error':
      return {
        ring: 'ring-rose-500/30',
        bg: 'bg-rose-950/20',
        text: 'text-rose-200',
        border: 'border-rose-900/60',
      };
    default:
      return {
        ring: 'ring-indigo-500/30',
        bg: 'bg-indigo-950/20',
        text: 'text-indigo-200',
        border: 'border-indigo-900/60',
      };
  }
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = React.useState<Toast[]>([]);

  const pushToast = React.useCallback((t: Omit<Toast, 'id' | 'createdAt'>) => {
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    const toast: Toast = {
      id,
      createdAt: Date.now(),
      ttlMs: t.ttlMs ?? 3500,
      title: t.title,
      message: t.message,
      tone: t.tone,
    };

    setToasts((prev) => [toast, ...prev].slice(0, 5));

    window.setTimeout(() => {
      setToasts((prev) => prev.filter((x) => x.id !== id));
    }, toast.ttlMs);
  }, []);

  return (
    <ToastContext.Provider value={{ pushToast }}>
      {children}
      <div className="fixed right-4 top-4 z-50 flex w-[360px] max-w-[calc(100vw-2rem)] flex-col gap-2">
        {toasts.map((t) => {
          const s = toneStyles(t.tone);
          return (
            <div
              key={t.id}
              className={`rounded border ${s.border} ${s.bg} p-3 shadow-lg ring-1 ${s.ring}`}
            >
              <div className={`text-sm font-semibold ${s.text}`}>{t.title}</div>
              {t.message ? <div className="mt-1 text-sm text-slate-300">{t.message}</div> : null}
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = React.useContext(ToastContext);
  if (!ctx) throw new Error('useToast must be used within ToastProvider');
  return ctx;
}

