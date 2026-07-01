import React, { useEffect, useState } from 'react';
import { getAlphas, createAlpha, AlphaResponse, AlphaCreate } from '../services/alphaEngineApi';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { RefreshCw } from 'lucide-react';


export function AlphaLabPage() {
  const [alphas, setAlphas] = useState<AlphaResponse[]>([]);
  const [selectedAlpha, setSelectedAlpha] = useState<AlphaResponse | null>(null);
  const [alphaText, setAlphaText] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAlphas = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getAlphas();
      setAlphas(response.items);
      if (response.items.length > 0 && !selectedAlpha) {
        setSelectedAlpha(response.items[0]);
        setAlphaText(response.items[0].expression);
      }
    } catch (err) {
      setError('Failed to fetch alphas. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlphas();
  }, []);

  const handleCreateAlpha = async () => {
    setIsCreating(true);
    setError(null);
    try {
      const newAlpha: AlphaCreate = {
        name: `New Alpha ${new Date().toISOString()}`,
        description: 'A new alpha created from the lab',
        expression: alphaText,
        status: 'pending',
      };
      await createAlpha(newAlpha);
      await fetchAlphas();
    } catch (err) {
      setError('Failed to create alpha.');
      console.error(err);
    } finally {
      setIsCreating(false);
    }
  };

  const handleSelectAlpha = (alpha: AlphaResponse) => {
    setSelectedAlpha(alpha);
    setAlphaText(alpha.expression);
  };

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Alpha Lab</h1>
        <Button onClick={fetchAlphas} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Alpha List */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Alphas</CardTitle>
            </CardHeader>
            <CardContent>
              {alphas.length === 0 ? (
                <p className="text-sm text-slate-500">No alphas found.</p>
              ) : (
                <ul className="space-y-2">
                  {alphas.map((alpha) => (
                    <li key={alpha.id}>
                      <button
                        onClick={() => handleSelectAlpha(alpha)}
                        className={`w-full text-left p-2 rounded-md ${selectedAlpha?.id === alpha.id ? 'bg-slate-700' : 'hover:bg-slate-800'}`}
                      >
                        {alpha.name}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Alpha Editor and Metrics */}
        <div className="lg:col-span-3 grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Alpha Editor</CardTitle>
              </CardHeader>
              <CardContent>
                <textarea
                  value={alphaText}
                  onChange={(e) => setAlphaText(e.target.value)}
                  className="h-72 w-full resize-none rounded border border-slate-800 bg-slate-950/40 p-3 font-mono text-sm text-slate-100 outline-none"
                  spellCheck={false}
                />
                <Button onClick={handleCreateAlpha} disabled={isCreating} className="mt-4">
                  {isCreating ? 'Creating...' : 'Create New Alpha from Editor'}
                </Button>
              </CardContent>
            </Card>
          </div>
          <div>
            <Card>
              <CardHeader>
                <CardTitle>Metrics</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {selectedAlpha ? (
                  <>
                    <div>
                      <p className="text-sm text-slate-400">Sharpe Ratio</p>
                      <p className="text-lg font-semibold">{selectedAlpha.sharpe?.toFixed(4) ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-400">Turnover</p>
                      <p className="text-lg font-semibold">{selectedAlpha.turnover?.toFixed(4) ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-400">Fitness</p>
                      <p className="text-lg font-semibold">{selectedAlpha.fitness?.toFixed(4) ?? 'N/A'}</p>
                    </div>
                    <div>
                      <p className="text-sm text-slate-400">Status</p>
                      <p className="text-lg font-semibold">{selectedAlpha.status}</p>
                    </div>
                  </>
                ) : (
                  <p className="text-sm text-slate-500">Select an alpha to view metrics.</p>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Equity Curve</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-500">
              No time-series equity curve data is available from the backend alpha_engine API.
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Drawdown</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-slate-500">
              No time-series drawdown data is available from the backend alpha_engine API.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

