import React from 'react';

type Props = {
  children: React.ReactNode;
};

type State = {
  hasError: boolean;
  error?: Error;
};

export class ErrorBoundary extends React.Component<Props, State> {
  state: State = {
    hasError: false,
    error: undefined,
  };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch() {
    // Intentionally left blank: could be wired to logging later.
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="m-6 rounded border border-rose-900/60 bg-rose-950/20 p-4">
          <div className="text-sm font-medium text-rose-300">Something went wrong</div>
          <div className="mt-1 text-sm text-slate-300">
            {this.state.error?.message ?? 'Unknown error'}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

