import React, { useState, useEffect } from 'react';
import { getAlphas, AlphaResponse } from '../services/alphaEngineApi';
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

export function AlphasPage() {
  const [alphas, setAlphas] = useState<AlphaResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAlphas = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getAlphas();
      setAlphas(response.items);
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

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-semibold">Alphas</h1>
        <Button onClick={fetchAlphas} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Alpha List</CardTitle>
        </CardHeader>
        <CardContent>
          {alphas.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <p>No alphas found.</p>
              <p className="text-sm mt-2">Create new alphas in the Alpha Lab to see data here.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Description</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Sharpe</TableHead>
                  <TableHead>Turnover</TableHead>
                  <TableHead>Fitness</TableHead>
                  <TableHead>Created At</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {alphas.map((alpha) => (
                  <TableRow key={alpha.id}>
                    <TableCell className="font-medium">{alpha.name}</TableCell>
                    <TableCell>{alpha.description || 'N/A'}</TableCell>
                    <TableCell>{alpha.status}</TableCell>
                    <TableCell>{alpha.sharpe?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{alpha.turnover?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{alpha.fitness?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{new Date(alpha.created_at).toLocaleString()}</TableCell>
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
