import React from 'react';
import { Modal, Table } from '../../../components/ui';
import { Order } from '../../../types';
import { formatCurrency, formatDate } from '../../../utils/format';
import { OrderStatusBadge } from './OrderStatusBadge';

interface OrderDetailsProps {
  order: Order | null;
  isOpen: boolean;
  onClose: () => void;
}

export const OrderDetails: React.FC<OrderDetailsProps> = ({
  order,
  isOpen,
  onClose
}) => {
  if (!order) return null;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Pedido #${order.id}`}
      size="lg"
    >
      <div className="space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <h3 className="text-sm font-medium text-gray-500">Cliente</h3>
            <p className="mt-1">{order.customer.name}</p>
            <p className="text-sm text-gray-500">{order.customer.email}</p>
            <p className="text-sm text-gray-500">{order.customer.phone}</p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500">Status</h3>
            <div className="mt-1">
              <OrderStatusBadge status={order.status} />
            </div>
            <p className="mt-1 text-sm text-gray-500">
              Criado em: {formatDate(order.created_at)}
            </p>
          </div>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-500 mb-2">Itens do Pedido</h3>
          <Table>
            <Table.Head>
              <Table.Row>
                <Table.Cell>Produto</Table.Cell>
                <Table.Cell>Quantidade</Table.Cell>
                <Table.Cell>Preço Unit.</Table.Cell>
                <Table.Cell>Total</Table.Cell>
              </Table.Row>
            </Table.Head>
            <Table.Body>
              {order.items.map((item, index) => (
                <Table.Row key={index}>
                  <Table.Cell>{item.product.name}</Table.Cell>
                  <Table.Cell>{item.quantity}</Table.Cell>
                  <Table.Cell>{formatCurrency(item.price)}</Table.Cell>
                  <Table.Cell>{formatCurrency(item.price * item.quantity)}</Table.Cell>
                </Table.Row>
              ))}
            </Table.Body>
          </Table>
        </div>

        <div className="border-t pt-4">
          <div className="flex justify-between">
            <span className="font-medium">Total do Pedido</span>
            <span className="font-bold">{formatCurrency(order.total)}</span>
          </div>
        </div>

        {order.notes && (
          <div>
            <h3 className="text-sm font-medium text-gray-500 mb-1">Observações</h3>
            <p className="text-sm text-gray-700">{order.notes}</p>
          </div>
        )}
      </div>
    </Modal>
  );
}; 