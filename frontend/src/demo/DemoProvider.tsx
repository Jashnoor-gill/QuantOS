import React, { createContext, useContext, useMemo, useState } from 'react';

type DemoContextValue = {
  enabled: boolean;
  setEnabled: (enabled: boolean) => void;
  toggle: () => void;
};

const DemoContext = createContext<DemoContextValue | null>(null);
const storageKey = 'quantos-demo-mode';

function readInitialValue() {
  return typeof window !== 'undefined' && window.localStorage.getItem(storageKey) !== 'off';
}

export function DemoProvider({ children }: { children: React.ReactNode }) {
  const [enabled, setEnabledState] = useState(readInitialValue);

  const setEnabled = (value: boolean) => {
    setEnabledState(value);
    window.localStorage.setItem(storageKey, value ? 'on' : 'off');
  };

  const value = useMemo(
    () => ({ enabled, setEnabled, toggle: () => setEnabled(!enabled) }),
    [enabled],
  );

  return <DemoContext.Provider value={value}>{children}</DemoContext.Provider>;
}

export function useDemoMode() {
  const context = useContext(DemoContext);
  if (!context) throw new Error('useDemoMode must be used inside DemoProvider');
  return context;
}