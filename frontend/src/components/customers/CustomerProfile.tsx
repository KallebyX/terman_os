import React, { useState } from 'react';
import { Card, Avatar, Tabs, Button } from '../ui';
import { CustomerDetails } from './CustomerDetails';
import { OrderHistory } from './OrderHistory';
import { LoyaltyPoints } from './LoyaltyPoints';
import { useCustomer } from '../../hooks/useCustomer';
import { Customer } from '../../types';

interface CustomerProfileProps {
  customerId: string;
}

export const CustomerProfile: React.FC<CustomerProfileProps> = ({ customerId }) => {
  const { customer, loading, error } = useCustomer(customerId);
  const [activeTab, setActiveTab] = useState('details');

  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro ao carregar perfil do cliente</div>;

  return (
    <Card className="p-4">
      <div className="flex items-center mb-6">
        <Avatar 
          src={customer.avatarUrl} 
          alt={customer.name}
          size="lg"
        />
        <div className="ml-4">
          <h2 className="text-2xl font-bold">{customer.name}</h2>
          <p className="text-gray-600">{customer.email}</p>
        </div>
      </div>

      <Tabs
        value={activeTab}
        onChange={setActiveTab}
        items={[
          { value: 'details', label: 'Detalhes' },
          { value: 'orders', label: 'Histórico de Pedidos' },
          { value: 'loyalty', label: 'Programa de Fidelidade' }
        ]}
      />

      <div className="mt-4">
        {activeTab === 'details' && <CustomerDetails customer={customer} />}
        {activeTab === 'orders' && <OrderHistory customerId={customerId} />}
        {activeTab === 'loyalty' && <LoyaltyPoints customer={customer} />}
      </div>
    </Card>
  );
}; 