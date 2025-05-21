import React from 'react';
import { DataTable } from '../../../components/shared/DataTable';
import { Badge } from '../../../components/ui';
import { Order } from '../../../types';
import { formatCurrency, formatDate } from '../../../utils/format';

interface OrderHistoryProps {
  orders: Order[];
  onViewDetails: (order: Order) => void;
}

export const OrderHistory: React.FC<OrderHistoryProps> = ({
  orders,
  onViewDetails
}) => {
  const columns = [
    {
      key: 'id',
      title: 'Pedido',
      render: (order: Order) => `#${order.id}`
    },
    {
      key: 'created_at',
      title: 'Data',
      render: (order: Order) => formatDate(order.created_at)
    },
    {
      key: 'total',
      title: 'Total',
      render: (order: Order) => formatCurrency(order.total)
    },
    {
      key: 'status',
      title: 'Status',
      render: (order: Order) => (
        <Badge
          color={
            order.status === 'completed'
              ? 'green'
              : order.status === 'cancelled'
              ? 'red'
              : 'yellow'
          }
        >
          {order.status === 'completed'
            ? 'Concluído'
            : order.status === 'cancelled'
            ? 'Cancelado'
            : 'Em andamento'}
        </Badge>
      )
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="p-4 border-b">
        <h2 className="text-lg font-medium">Histórico de Pedidos</h2>
      </div>
      <div className="p-4">
        <DataTable
          data={orders}
          columns={columns}
          onRowClick={onViewDetails}
        />
      </div>
    </div>
  );
}; 