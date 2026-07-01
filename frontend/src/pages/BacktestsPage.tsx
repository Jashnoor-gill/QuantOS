import React, { useState, useEffect } from 'react';
import { getBacktests, BacktestResponse } from '../services/backtestingEngineApi';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '../components/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { RefreshCw } from 'lucide-react';

export function BacktestsPage() {
  const [backtests, setBacktests] = useState<BacktestResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBacktests = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getBacktests();
      setBacktests(response.items);
    } catch (err) {
      setError('Failed to fetch backtests. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBacktests();
  }, []);

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Backtests</h1>
        <Button onClick={fetchBacktests} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Backtest List</CardTitle>
        </CardHeader>
        <CardContent>
          {backtests.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <p>No backtests found.</p>
              <p className="text-sm mt-2">Run a strategy backtest to see data here.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Strategy ID</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Start Date</TableHead>
                  <TableHead>End Date</TableHead>
                  <TableHead>Initial Capital</TableHead>
                  <TableHead>Final Capital</TableHead>
                  <TableHead>Total Return</TableHead>
                  <TableHead>Sharpe Ratio</TableHead>
                  <TableHead>Max Drawdown</TableHead>
                  <TableHead>Created At</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {backtests.map((backtest) => (
                  <TableRow key={backtest.id}>
                    <TableCell className="font-medium">{backtest.strategy_id}</TableCell>
                    <TableCell>{backtest.status}</TableCell>
                    <TableCell>{new Date(backtest.start_date).toLocaleDateString()}</TableCell>
                    <TableCell>{new Date(backtest.end_date).toLocaleDateString()}</TableCell>
                    <TableCell>{backtest.initial_capital.toFixed(2)}</TableCell>
                    <TableCell>{backtest.final_capital.toFixed(2)}</TableCell>
                    <TableCell>{backtest.total_return ? (backtest.total_return * 100).toFixed(2) + '%' : 'N/A'}</TableCell>
                    <TableCell>{backtest.sharpe_ratio?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{backtest.max_drawdown ? (backtest.max_drawdown * 100).toFixed(2) + '%' : 'N/A'}</TableCell>
                    <TableCell>{new Date(backtest.created_at).toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
