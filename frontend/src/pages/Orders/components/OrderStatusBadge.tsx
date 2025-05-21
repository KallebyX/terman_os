import React from 'react';
import { Badge } from '../../../components/ui';

type OrderStatus = 'pending' | 'processing' | 'completed' | 'cancelled';

interface OrderStatusBadgeProps {
  status: OrderStatus;
}

export const OrderStatusBadge: React.FC<OrderStatusBadgeProps> = ({ status }) => {
  const statusConfig = {
    pending: { color: 'yellow', label: 'Pendente' },
    processing: { color: 'blue', label: 'Em Processamento' },
    completed: { color: 'green', label: 'Concluído' },
    cancelled: { color: 'red', label: 'Cancelado' }
  };

  const config = statusConfig[status];

  return (
    <Badge color={config.color}>
      {config.label}
    </Badge>
  );
}; 