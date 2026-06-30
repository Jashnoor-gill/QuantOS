import React, { useState, useEffect } from 'react';
import { listAssets, ingestData, getHistory, PriceBar, Asset, createAsset } from '../services/marketDataApi';
import { useQuery, useMutation, useQueryClient } from 'react-query';

export function MarketDataPage() {
  const queryClient = useQueryClient();
  const [selectedAsset, setSelectedAsset] = useState<string>('');
  const [newAssetSymbol, setNewAssetSymbol] = useState<string>('');

  const { data: assets, isLoading: isLoadingAssets } = useQuery('assets', listAssets);

  const { data: history, isLoading: isLoadingHistory } = useQuery(
    ['history', selectedAsset],
    () => getHistory(selectedAsset),
    {
      enabled: !!selectedAsset,
    }
  );

  const ingestMutation = useMutation((symbol: string) => ingestData(symbol), {
    onSuccess: () => {
      queryClient.invalidateQueries(['history', selectedAsset]);
    },
  });

  const createAssetMutation = useMutation((symbol: string) => createAsset(symbol), {
      onSuccess: () => {
          queryClient.invalidateQueries('assets');
          setNewAssetSymbol('');
      }
  });

  const handleIngest = () => {
    if (selectedAsset) {
      ingestMutation.mutate(selectedAsset);
    }
  };

  const handleCreateAsset = () => {
      if(newAssetSymbol) {
          createAssetMutation.mutate(newAssetSymbol);
      }
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold">Market Data</h1>
      
      <div className="mt-4">
        <label htmlFor="asset" className="block text-sm font-medium text-slate-300">
          Select Asset
        </label>
        <select
          id="asset"
          name="asset"
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md bg-slate-800"
          value={selectedAsset}
          onChange={(e) => setSelectedAsset(e.target.value)}
          disabled={isLoadingAssets}
        >
          <option value="">{isLoadingAssets ? 'Loading...' : 'Select an asset'}</option>
          {assets?.items.map((asset) => (
            <option key={asset.id} value={asset.symbol}>
              {asset.symbol}
            </option>
          ))}
        </select>
      </div>

        <div className="mt-4">
            <label htmlFor="new-asset" className="block text-sm font-medium text-slate-300">
            Add New Asset
            </label>
            <div className="mt-1 flex rounded-md shadow-sm">
            <input
                type="text"
                name="new-asset"
                id="new-asset"
                className="focus:ring-indigo-500 focus:border-indigo-500 block w-full rounded-none rounded-l-md sm:text-sm border-gray-300 bg-slate-800"
                placeholder="e.g., AAPL"
                value={newAssetSymbol}
                onChange={(e) => setNewAssetSymbol(e.target.value)}
            />
            <button
                onClick={handleCreateAsset}
                disabled={createAssetMutation.isLoading}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-r-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
            >
                {createAssetMutation.isLoading ? 'Adding...' : 'Add Asset'}
            </button>
            </div>
        </div>

      <div className="mt-4">
        <button
          onClick={handleIngest}
          disabled={!selectedAsset || ingestMutation.isLoading}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {ingestMutation.isLoading ? 'Ingesting...' : 'Ingest Data for Selected Asset'}
        </button>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold">Historical Data</h2>
        {isLoadingHistory && <p>Loading history...</p>}
        {ingestMutation.isSuccess && <p className="text-green-500">Ingestion successful!</p>}
        {ingestMutation.isError && <p className="text-red-500">Ingestion failed.</p>}
        
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-700">
            <thead className="bg-gray-800">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Timestamp</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Open</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">High</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Low</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Close</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider">Volume</th>
              </tr>
            </thead>
            <tbody className="bg-gray-900 divide-y divide-gray-800">
              {history?.items.map((bar) => (
                <tr key={bar.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-400">{new Date(bar.timestamp).toLocaleString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{bar.open}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{bar.high}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{bar.low}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{bar.close}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{bar.volume}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

