import React from 'react';
import { Table, Badge } from '../../../components/ui';
import { formatCurrency, formatDate } from '../../../utils/format';

interface Order {
  id: number;
  customer: string;
  total: number;
  status: string;
  created_at: string;
}

interface RecentOrdersProps {
  orders: Order[];
}

export const RecentOrders: React.FC<RecentOrdersProps> = ({ orders }) => {
  const getStatusColor = (status: string) => {
    const colors = {
      pending: 'yellow',
      processing: 'blue',
      completed: 'green',
      cancelled: 'red'
    };
    return colors[status.toLowerCase()] || 'gray';
  };

  return (
    <Table>
      <Table.Head>
        <Table.Row>
          <Table.Cell>Pedido</Table.Cell>
          <Table.Cell>Cliente</Table.Cell>
          <Table.Cell>Total</Table.Cell>
          <Table.Cell>Status</Table.Cell>
          <Table.Cell>Data</Table.Cell>
        </Table.Row>
      </Table.Head>
      <Table.Body>
        {orders.map((order) => (
          <Table.Row key={order.id}>
            <Table.Cell>#{order.id}</Table.Cell>
            <Table.Cell>{order.customer}</Table.Cell>
            <Table.Cell>{formatCurrency(order.total)}</Table.Cell>
            <Table.Cell>
              <Badge color={getStatusColor(order.status)}>
                {order.status}
              </Badge>
            </Table.Cell>
            <Table.Cell>{formatDate(order.created_at)}</Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
}; 