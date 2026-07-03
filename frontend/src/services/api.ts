import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://13.61.182.81:8000',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export type HealthResponse = {
  status: string;
  app: string;
  version: string;
};

export async function getHealth(): Promise<HealthResponse> {
  const res = await api.get<HealthResponse>('/health');
  return res.data;
}
