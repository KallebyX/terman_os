import React from 'react';
import { Navigate, RouteObject } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';
import { AuthLayout } from '../layouts/AuthLayout';
import { LoginPage } from '../pages/Auth/LoginPage';
import { RegisterPage } from '../pages/Auth/RegisterPage';
import { ForgotPasswordPage } from '../pages/Auth/ForgotPasswordPage';
import { ResetPasswordPage } from '../pages/Auth/ResetPasswordPage';
import { DashboardPage } from '../pages/Dashboard/DashboardPage';
import { ProductsPage } from '../pages/Products/ProductsPage';
import { CustomersPage } from '../pages/Customers/CustomersPage';
import { OrdersPage } from '../pages/Orders/OrdersPage';
import { PDVPage } from '../pages/PDV/PDVPage';
import { ReportsPage } from '../pages/Reports/ReportsPage';
import { SettingsPage } from '../pages/Settings/SettingsPage';
import { useAuth } from '../contexts/AuthContext';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
};

const AdminRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (!user || user.role !== 'admin') {
    return <Navigate to="/dashboard" replace />;
  }

  return <>{children}</>;
};

export const routes: RouteObject[] = [
  {
    path: '/',
    element: <AuthLayout />,
    children: [
      { path: 'login', element: <LoginPage /> },
      { path: 'register', element: <RegisterPage /> },
      { path: 'forgot-password', element: <ForgotPasswordPage /> },
      { path: 'reset-password', element: <ResetPasswordPage /> },
      { path: '', element: <Navigate to="/login" replace /> }
    ]
  },
  {
    path: '/app',
    element: (
      <PrivateRoute>
        <MainLayout />
      </PrivateRoute>
    ),
    children: [
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'pdv', element: <PDVPage /> },
      { path: 'produtos', element: <ProductsPage /> },
      { path: 'clientes', element: <CustomersPage /> },
      { path: 'pedidos', element: <OrdersPage /> },
      {
        path: 'relatorios',
        element: (
          <AdminRoute>
            <ReportsPage />
          </AdminRoute>
        )
      },
      {
        path: 'configuracoes',
        element: (
          <AdminRoute>
            <SettingsPage />
          </AdminRoute>
        )
      },
      { path: '', element: <Navigate to="/app/dashboard" replace /> }
    ]
  }
]; 