import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LoadingState } from './LoadingState';

export const ProtectedRoute = () => {
  const { token, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingState />;
  }

  if (!token) {
    return <Navigate to="/login" />;
  }

  return <Outlet />;
};
