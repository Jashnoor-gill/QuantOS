import React, { useState, useEffect } from 'react';
import { getFactorExposures, FactorExposure } from '../services/factorEngineApi';
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

export function FactorsPage() {
  const [factors, setFactors] = useState<FactorExposure[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchFactors = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getFactorExposures();
      setFactors(response.items);
    } catch (err) {
      setError('Failed to fetch factors. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchFactors();
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
        <h1 className="text-2xl font-semibold">Factor Exposures</h1>
        <Button onClick={fetchFactors} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Factor Exposure List</CardTitle>
        </CardHeader>
        <CardContent>
          {factors.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <p>No factor exposures found.</p>
              <p className="text-sm mt-2">Run the factor engine to see data here.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Factor Name</TableHead>
                  <TableHead>Symbol</TableHead>
                  <TableHead className="text-right">Exposure</TableHead>
                  <TableHead>Created At</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {factors.map((factor) => (
                  <TableRow key={factor.id}>
                    <TableCell className="font-medium">{factor.factor_name}</TableCell>
                    <TableCell>{factor.symbol}</TableCell>
                    <TableCell className="text-right">{factor.exposure.toFixed(4)}</TableCell>
                    <TableCell>{new Date(factor.created_at).toLocaleString()}</TableCell>
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
