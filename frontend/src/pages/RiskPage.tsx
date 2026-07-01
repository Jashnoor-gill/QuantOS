import React, { useState, useEffect } from 'react';
import { getRiskMetrics, RiskMetricResponse } from '../services/riskEngineApi';
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

export function RiskPage() {
  const [riskMetrics, setRiskMetrics] = useState<RiskMetricResponse[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRiskMetrics = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getRiskMetrics();
      setRiskMetrics(response.items);
    } catch (err) {
      setError('Failed to fetch risk metrics. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRiskMetrics();
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
        <h1 className="text-2xl font-semibold">Risk Metrics</h1>
        <Button onClick={fetchRiskMetrics} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Risk Metric List</CardTitle>
        </CardHeader>
        <CardContent>
          {riskMetrics.length === 0 ? (
            <div className="text-center py-12 text-slate-500">
              <p>No risk metrics found.</p>
              <p className="text-sm mt-2">Run risk analysis to see data here.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Portfolio ID</TableHead>
                  <TableHead>VaR 95</TableHead>
                  <TableHead>VaR 99</TableHead>
                  <TableHead>Expected Shortfall</TableHead>
                  <TableHead>Beta</TableHead>
                  <TableHead>Volatility</TableHead>
                  <TableHead>Max Drawdown</TableHead>
                  <TableHead>Risk Score</TableHead>
                  <TableHead>Created At</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {riskMetrics.map((metric) => (
                  <TableRow key={metric.id}>
                    <TableCell className="font-medium">{metric.portfolio_id}</TableCell>
                    <TableCell>{metric.var_95?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{metric.var_99?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{metric.expected_shortfall?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{metric.beta?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{metric.volatility?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{metric.max_drawdown?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{metric.risk_score?.toFixed(4) || 'N/A'}</TableCell>
                    <TableCell>{new Date(metric.created_at).toLocaleString()}</TableCell>
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
