import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Páginas
import LandingPage from './pages/Landing/LandingPage';
import MarketplacePage from './pages/Marketplace/MarketplacePage';
import DashboardPage from './pages/dashboard/DashboardPage';
import PDVPage from './pages/PDV/PDVPage';
import InventoryPage from './pages/inventory/InventoryPage';
import LoginPage from './pages/Client/LoginPage';
import ClientDashboard from './pages/Client/ClientDashboard';
import NotFoundPage from './pages/NotFound';

// Layouts
import { AdminLayout, AuthLayout } from './layouts/BaseLayouts';

// Estilos globais
import './styles/global.css';

// Componente de proteção de rotas
const ProtectedRoute = ({ children, requiredRole }) => {
  const { isAuthenticated, userRole } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (requiredRole && userRole !== requiredRole) {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Página inicial - Landing Page */}
          <Route path="/" element={<LandingPage />} />
          
          {/* Autenticação */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Marketplace */}
          <Route path="/marketplace" element={<MarketplacePage />} />
          <Route path="/marketplace/product/:id" element={<MarketplacePage />} />
          <Route path="/marketplace/cart" element={<MarketplacePage />} />
          <Route path="/marketplace/checkout" element={<MarketplacePage />} />
          
          {/* Área do Cliente */}
          <Route 
            path="/client" 
            element={
              <ProtectedRoute requiredRole="client">
                <ClientDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/client/orders" 
            element={
              <ProtectedRoute requiredRole="client">
                <ClientDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/client/profile" 
            element={
              <ProtectedRoute requiredRole="client">
                <ClientDashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Sistema Administrativo */}
          <Route 
            path="/admin" 
            element={
              <ProtectedRoute requiredRole="admin">
                <Navigate to="/admin/dashboard" replace />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/dashboard" 
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminLayout>
                  <DashboardPage />
                </AdminLayout>
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/pdv" 
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminLayout>
                  <PDVPage />
                </AdminLayout>
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/admin/inventory" 
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminLayout>
                  <InventoryPage />
                </AdminLayout>
              </ProtectedRoute>
            } 
          />
          
          {/* Rotas legadas para compatibilidade */}
          <Route path="/pdv" element={<Navigate to="/admin/pdv" replace />} />
          <Route path="/inventory" element={<Navigate to="/admin/inventory" replace />} />
          
          {/* Página 404 para rotas não encontradas */}
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
