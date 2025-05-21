import React from 'react';
import { Card } from '../ui/Card';
import { Table, Thead, Tbody, Th, Td } from '../ui/Table';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { formatCurrency, formatDateTime } from '../../utils/formatters';

interface Order {
  id: string;
  customer: {
    name: string;
    phone: string;
  };
  items: Array<{
    name: string;
    quantity: number;
    price: number;
  }>;
  total: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  paymentMethod: string;
  createdAt: string;
}

interface OrderListProps {
  orders: Order[];
  onViewDetails: (orderId: string) => void;
  onUpdateStatus: (orderId: string, status: Order['status']) => void;
  loading?: boolean;
}

export const OrderList: React.FC<OrderListProps> = ({
  orders,
  onViewDetails,
  onUpdateStatus,
  loading
}) => {
  const getStatusBadge = (status: Order['status']) => {
    const variants = {
      pending: 'warning',
      processing: 'info',
      completed: 'success',
      cancelled: 'danger'
    };

    const labels = {
      pending: 'Pendente',
      processing: 'Em Processamento',
      completed: 'Concluído',
      cancelled: 'Cancelado'
    };

    return <Badge variant={variants[status]}>{labels[status]}</Badge>;
  };

  if (loading) {
    return (
      <Card>
        <div className="p-4 animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4" />
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-gray-200 rounded" />
            ))}
          </div>
        </div>
      </Card>
    );
  }

  return (
    <Card>
      <div className="p-4">
        <Table>
          <Thead>
            <tr>
              <Th>Pedido</Th>
              <Th>Cliente</Th>
              <Th>Total</Th>
              <Th>Status</Th>
              <Th>Data</Th>
              <Th>Ações</Th>
            </tr>
          </Thead>
          <Tbody>
            {orders.map(order => (
              <tr key={order.id}>
                <Td>#{order.id.slice(-6)}</Td>
                <Td>
                  <div>
                    <p className="font-medium text-gray-900">{order.customer.name}</p>
                    <p className="text-sm text-gray-500">{order.customer.phone}</p>
                  </div>
                </Td>
                <Td>{formatCurrency(order.total)}</Td>
                <Td>{getStatusBadge(order.status)}</Td>
                <Td>{formatDateTime(order.createdAt)}</Td>
                <Td>
                  <div className="flex space-x-2">
                    <Button
                      variant="secondary"
                      size="sm"
                      onClick={() => onViewDetails(order.id)}
                    >
                      Detalhes
                    </Button>
                    {order.status === 'pending' && (
                      <>
                        <Button
                          variant="success"
                          size="sm"
                          onClick={() => onUpdateStatus(order.id, 'processing')}
                        >
                          Processar
                        </Button>
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => onUpdateStatus(order.id, 'cancelled')}
                        >
                          Cancelar
                        </Button>
                      </>
                    )}
                    {order.status === 'processing' && (
                      <Button
                        variant="success"
                        size="sm"
                        onClick={() => onUpdateStatus(order.id, 'completed')}
                      >
                        Concluir
                      </Button>
                    )}
                  </div>
                </Td>
              </tr>
            ))}
          </Tbody>
        </Table>
      </div>
    </Card>
  );
}; 