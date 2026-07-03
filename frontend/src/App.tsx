import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import { Layout } from './components/Layout';
import { LoginPage } from './pages/LoginPage';
import { ProtectedRoute } from './components/ProtectedRoute';
import { IndexRoutes } from './routes';

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />

          {IndexRoutes.map((r) => (
            <Route
              key={r.path}
              path={r.path.replace('/', '')}
              element={r.element}
            />
          ))}
        </Route>
      </Route>
    </Routes>
  );
}
