import React, { useState, useEffect } from 'react';
import { getReports, ReportResponse } from '../services/reportingApi';
import { LoadingState } from '../components/LoadingState';
import { ErrorState } from '../components/ErrorState';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { RefreshCw } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';

export function ReportsPage() {
  const [reports, setReports] = useState<ReportResponse[]>([]);
  const [selectedReport, setSelectedReport] = useState<ReportResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchReports = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getReports();
      setReports(response.items);
      if (response.items.length > 0 && !selectedReport) {
        setSelectedReport(response.items[0]);
      }
    } catch (err) {
      setError('Failed to fetch reports. Please try again later.');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
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
        <h1 className="text-2xl font-semibold">Reports</h1>
        <Button onClick={fetchReports} variant="outline" size="sm">
          <RefreshCw className="h-4 w-4 mr-2" />
          Refresh
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <CardTitle>Report List</CardTitle>
            </CardHeader>
            <CardContent>
              {reports.length === 0 ? (
                <p className="text-sm text-slate-500">No reports found.</p>
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Title</TableHead>
                      <TableHead>Status</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {reports.map((report) => (
                      <TableRow
                        key={report.id}
                        onClick={() => setSelectedReport(report)}
                        className={`cursor-pointer ${selectedReport?.id === report.id ? 'bg-slate-700' : 'hover:bg-slate-800'}`}
                      >
                        <TableCell className="font-medium">{report.title}</TableCell>
                        <TableCell>{report.status || 'N/A'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Report Details</CardTitle>
            </CardHeader>
            <CardContent>
              {selectedReport ? (
                <div>
                  <h2 className="text-lg font-semibold">{selectedReport.title}</h2>
                  <p className="text-sm text-slate-400">
                    Created: {new Date(selectedReport.created_at).toLocaleString()}
                  </p>
                  <p className="text-sm text-slate-400">
                    Status: {selectedReport.status || 'N/A'}
                  </p>
                  <div className="mt-4 prose prose-invert max-w-none">
                    <p>{selectedReport.content}</p>
                  </div>
                  <div className="mt-4 text-sm text-slate-500">
                    Report content is displayed as stored by the backend.
                  </div>

                </div>
              ) : (
                <p className="text-sm text-slate-500">Select a report to view details.</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
