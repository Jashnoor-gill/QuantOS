import axios from 'axios';

export const api = axios.create({
  // Backend routes do NOT include an /api prefix.
  baseURL: '',
});


export type HealthResponse = { status: string; app: string; version: string };

export async function getHealth(): Promise<HealthResponse> {
  const res = await api.get<HealthResponse>('/health');
  return res.data;
}

