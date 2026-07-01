import { api } from './api';

export interface ReportResponse {
  id: number;
  title: string;
  report_type: string | null;
  content: string;
  generated_by: string | null;
  status: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReportListResponse {
  items: ReportResponse[];
}

export const getReports = async (): Promise<ReportListResponse> => {
  const response = await api.get('/reporting/research-reports');
  return response.data;
};

export const getReport = async (id: number): Promise<ReportResponse> => {
  const response = await api.get(`/reporting/research-reports/${id}`);
  return response.data;
};
