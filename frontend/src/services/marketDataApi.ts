import { api } from './api';

export interface PriceBar {
  id: number;
  asset_id: number;
  timestamp: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface PriceBarListResponse {
  items: PriceBar[];
}

export interface Asset {
  id: number;
  symbol: string;
  name: string;
  asset_type: string;
  exchange: string;
}

export interface AssetListResponse {
  items: Asset[];
}

export async function ingestData(symbol: string): Promise<any> {
  const res = await api.post(`/market-data/ingest/${symbol}`);
  return res.data;
}

export async function ingestAllData(): Promise<any> {
  const res = await api.post('/market-data/ingest-all');
  return res.data;
}

export async function getHistory(symbol: string): Promise<PriceBarListResponse> {
  const res = await api.get<PriceBarListResponse>(`/market-data/history/${symbol}`);
  return res.data;
}

export async function listAssets(): Promise<AssetListResponse> {
  const res = await api.get<AssetListResponse>('/market-data/assets');
  return res.data;
}

export async function createAsset(symbol: string): Promise<Asset> {
    const res = await api.post<Asset>('/market-data/assets', { symbol: symbol, name: symbol, asset_type: 'stock', exchange: 'NASDAQ' });
    return res.data;
}
