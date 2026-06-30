import React, { useState } from 'react';
import {
  runMeanVarianceOptimization,
  runMinVariancePortfolio,
  runRiskParityPortfolio,
  fetchEfficientFrontier,
  OptimizeResponse,
  EfficientFrontierResponse,
  AssetReturn,
} from '../services/portfolioApi';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ScatterChart, Scatter, ZAxis } from 'recharts';

// Mock data for asset returns
const mockAssetReturns: AssetReturn[] = [
  { asset_id: 'AAPL', returns: [0.01, 0.02, -0.01, 0.03, 0.005] },
  { asset_id: 'GOOG', returns: [0.02, 0.03, 0.01, 0.02, 0.015] },
  { asset_id: 'MSFT', returns: [-0.01, 0.01, 0.02, 0.01, 0.025] },
];

export function PortfolioPage() {
  const [optimizationMethod, setOptimizationMethod] = useState('mean-variance');
  const [optimizationResult, setOptimizationResult] = useState<OptimizeResponse | null>(null);
  const [efficientFrontier, setEfficientFrontier] = useState<EfficientFrontierResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleOptimize = async () => {
    setIsLoading(true);
    setOptimizationResult(null);
    setEfficientFrontier(null);

    const payload = { returns: mockAssetReturns };

    try {
      let result: OptimizeResponse;
      if (optimizationMethod === 'mean-variance') {
        result = await runMeanVarianceOptimization(payload);
      } else if (optimizationMethod === 'min-variance') {
        result = await runMinVariancePortfolio(payload);
      } else {
        result = await runRiskParityPortfolio(payload);
      }
      setOptimizationResult(result);

      const frontier = await fetchEfficientFrontier(payload);
      setEfficientFrontier(frontier);
    } catch (error) {
      console.error('Optimization failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-semibold">Portfolio Optimization</h1>
      <div className="mt-4">
        <label htmlFor="optimizationMethod" className="block text-sm font-medium text-slate-300">
          Optimization Method
        </label>
        <select
          id="optimizationMethod"
          name="optimizationMethod"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md bg-slate-800"
          value={optimizationMethod}
          onChange={(e) => setOptimizationMethod(e.target.value)}
        >
          <option value="mean-variance">Mean-Variance</option>
          <option value="min-variance">Minimum Variance</option>
          <option value="risk-parity">Risk Parity</option>
        </select>
      </div>
      <div className="mt-4">
        <button
          onClick={handleOptimize}
          disabled={isLoading}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? 'Optimizing...' : 'Run Optimization'}
        </button>
      </div>

      {optimizationResult && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold">Optimization Results</h2>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-slate-800 p-4 rounded-lg">
              <h3 className="text-lg font-medium">Expected Return</h3>
              <p className="mt-2 text-2xl font-semibold text-green-400">
                {(optimizationResult.expected_return * 100).toFixed(2)}%
              </p>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg">
              <h3 className="text-lg font-medium">Volatility</h3>
              <p className="mt-2 text-2xl font-semibold text-red-400">
                {(optimizationResult.volatility * 100).toFixed(2)}%
              </p>
            </div>
            <div className="bg-slate-800 p-4 rounded-lg">
              <h3 className="text-lg font-medium">Sharpe Ratio</h3>
              <p className="mt-2 text-2xl font-semibold text-blue-400">
                {optimizationResult.sharpe_ratio.toFixed(4)}
              </p>
            </div>
          </div>

          <div className="mt-8">
            <h3 className="text-lg font-medium">Portfolio Weights</h3>
            <div className="mt-4">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={Object.entries(optimizationResult.weights).map(([name, value]) => ({ name, value }))}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" name="Weight" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {efficientFrontier && (
        <div className="mt-8">
          <h2 className="text-xl font-semibold">Efficient Frontier</h2>
          <div className="mt-4" style={{ width: '100%', height: 400 }}>
            <ResponsiveContainer>
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid />
                <XAxis type="number" dataKey="volatility" name="Volatility" unit="" />
                <YAxis type="number" dataKey="return_val" name="Return" unit="" />
                <ZAxis type="number" dataKey="sharpe_ratio" name="Sharpe Ratio" />
                <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                <Legend />
                <Scatter name="Efficient Frontier" data={efficientFrontier.points} fill="#8884d8" />
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}

