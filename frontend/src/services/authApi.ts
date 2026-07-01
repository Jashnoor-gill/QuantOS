import { api } from './api';

export interface User {
  id: number;
  email: string;
  username: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  refresh_token: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export const login = async (credentials: LoginRequest): Promise<TokenResponse> => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const register = async (userInfo: RegisterRequest): Promise<User> => {
  const response = await api.post('/auth/register', userInfo);
  return response.data;
};

export const getMe = async (): Promise<{ user: string }> => {
  const response = await api.get('/auth/me');
  return response.data;
};

