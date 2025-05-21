import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Card } from '../ui';
import { SalesReport } from './SalesReport';
import { FinancialReport } from './FinancialReport';
import { InventoryReport } from './InventoryReport';
import { CustomerReport } from './CustomerReport';

export const AdminReportView: React.FC = () => {
  const { user } = useAuth();

  // Verifica se o usuário tem permissão de admin
  if (!user?.isAdmin) {
    return (
      <Card className="p-4">
        <p className="text-red-600">Você não tem permissão para acessar esta área.</p>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Painel Administrativo</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <SalesReport adminView={true} />
        <FinancialReport />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <InventoryReport />
        <CustomerReport />
      </div>
    </div>
  );
}; 