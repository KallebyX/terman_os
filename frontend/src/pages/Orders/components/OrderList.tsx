import React from 'react';
import { DataTable } from '../../../components/shared/DataTable';
import { Button } from '../../../components/ui';
import { Order } from '../../../types';
import { formatCurrency, formatDate } from '../../../utils/format';
import { OrderStatusBadge } from './OrderStatusBadge';

interface OrderListProps {
  orders: Order[];
  onViewDetails: (order: Order) => void;
  onUpdateStatus: (orderId: number, status: Order['status']) => void;
}

export const OrderList: React.FC<OrderListProps> = ({
  orders,
  onViewDetails,
  onUpdateStatus
}) => {
  const columns = [
    {
      key: 'id',
      title: 'Pedido',
      render: (order: Order) => `#${order.id}`
    },
    {
      key: 'customer',
      title: 'Cliente',
      render: (order: Order) => order.customer.name
    },
    {
      key: 'total',
      title: 'Total',
      render: (order: Order) => formatCurrency(order.total)
    },
    {
      key: 'status',
      title: 'Status',
      render: (order: Order) => <OrderStatusBadge status={order.status} />
    },
    {
      key: 'created_at',
      title: 'Data',
      render: (order: Order) => formatDate(order.created_at)
    },
    {
      key: 'actions',
      title: 'Ações',
      render: (order: Order) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="outline"
            onClick={() => onViewDetails(order)}
          >
            Detalhes
          </Button>
          <select
            value={order.status}
            onChange={(e) => onUpdateStatus(order.id, e.target.value as Order['status'])}
            className="form-select text-sm"
          >
            <option value="pending">Pendente</option>
            <option value="processing">Em Processamento</option>
            <option value="completed">Concluído</option>
            <option value="cancelled">Cancelado</option>
          </select>
        </div>
      )
    }
  ];

  return (
    <DataTable
      data={orders}
      columns={columns}
    />
  );
}; 