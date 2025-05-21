import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Card } from '../ui';
import { ClientOrdersReport } from './ClientOrdersReport';
import { ClientLoyaltyReport } from './ClientLoyaltyReport';

export const ClientReportView: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return (
      <Card className="p-4">
        <p className="text-red-600">Faça login para acessar seus relatórios.</p>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Meus Relatórios</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ClientOrdersReport />
        <ClientLoyaltyReport />
      </div>
    </div>
  );
}; 