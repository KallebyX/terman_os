import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { formatCurrency, formatDateTime } from '../../utils/formatters';

interface Order {
  id: string;
  customer: {
    name: string;
  };
  total: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  createdAt: string;
}

interface RecentOrdersProps {
  orders: Order[];
  loading?: boolean;
}

export const RecentOrders: React.FC<RecentOrdersProps> = ({ orders, loading }) => {
  const getStatusBadge = (status: Order['status']) => {
    switch (status) {
      case 'completed':
        return <Badge variant="success">Concluído</Badge>;
      case 'processing':
        return <Badge variant="warning">Em Processamento</Badge>;
      case 'pending':
        return <Badge variant="default">Pendente</Badge>;
      case 'cancelled':
        return <Badge variant="danger">Cancelado</Badge>;
    }
  };

  if (loading) {
    return (
      <Card>
        <div className="p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Pedidos Recentes
          </h3>
          <div className="animate-pulse space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-gray-200 rounded-lg" />
            ))}
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <div className="p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Pedidos Recentes
        </h3>
        <div className="space-y-4">
          {orders.map(order => (
            <div
              key={order.id}
              className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
            >
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-medium">#{order.id.slice(-6)}</span>
                  {getStatusBadge(order.status)}
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  {order.customer.name}
                </p>
                <p className="text-xs text-gray-500">
                  {formatDateTime(order.createdAt)}
                </p>
              </div>
              <div className="text-right">
                <p className="font-medium text-gray-900">
                  {formatCurrency(order.total)}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}; 