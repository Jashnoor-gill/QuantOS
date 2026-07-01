import React, { useState, useEffect } from 'react';
import { getStrategies, StrategyResponse } from '../services/strategyEngineApi';
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

export function StrategiesPage() {
  const [strategies, setStrategies] = useState<StrategyResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStrategies = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getStrategies();
      setStrategies(response.items);
    } catch (err) {
      setError('Failed to fetch strategies. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStrategies();
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
        <h1 className="text-2xl font-semibold">Strategies</h1>
        <Button onClick={fetchStrategies} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Strategy List</CardTitle>
        </CardHeader>
        <CardContent>
          {strategies.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <p>No strategies found.</p>
              <p className="text-sm mt-2">Create new strategies to see data here.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Alpha ID</TableHead>
                  <TableHead>Rebalance Freq.</TableHead>
                  <TableHead>Created At</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {strategies.map((strategy) => (
                  <TableRow key={strategy.id}>
                    <TableCell className="font-medium">{strategy.name}</TableCell>
                    <TableCell>{strategy.strategy_type}</TableCell>
                    <TableCell>{strategy.status}</TableCell>
                    <TableCell>{strategy.alpha_id}</TableCell>
                    <TableCell>{strategy.rebalance_frequency || 'N/A'}</TableCell>
                    <TableCell>{new Date(strategy.created_at).toLocaleString()}</TableCell>
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
