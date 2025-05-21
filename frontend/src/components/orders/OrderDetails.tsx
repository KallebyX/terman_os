import React from 'react';
import { Modal } from '../ui/Modal';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { formatCurrency, formatDateTime } from '../../utils/formatters';

interface OrderDetailsProps {
  isOpen: boolean;
  onClose: () => void;
  order: {
    id: string;
    customer: {
      name: string;
      phone: string;
      email: string;
    };
    items: Array<{
      name: string;
      quantity: number;
      price: number;
    }>;
    total: number;
    status: string;
    paymentMethod: string;
    createdAt: string;
  };
  onPrint: () => void;
}

export const OrderDetails: React.FC<OrderDetailsProps> = ({
  isOpen,
  onClose,
  order,
  onPrint
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`Pedido #${order.id.slice(-6)}`}
    >
      <div className="space-y-6">
        <Card>
          <div className="p-4">
            <h4 className="text-sm font-medium text-gray-500 mb-2">
              Informações do Cliente
            </h4>
            <div className="space-y-1">
              <p className="font-medium text-gray-900">{order.customer.name}</p>
              <p className="text-gray-600">{order.customer.phone}</p>
              <p className="text-gray-600">{order.customer.email}</p>
            </div>
          </div>
        </Card>

        <Card>
          <div className="p-4">
            <h4 className="text-sm font-medium text-gray-500 mb-4">
              Itens do Pedido
            </h4>
            <div className="space-y-3">
              {order.items.map((item, index) => (
                <div
                  key={index}
                  className="flex justify-between items-center py-2 border-b border-gray-200 last:border-0"
                >
                  <div>
                    <p className="font-medium text-gray-900">{item.name}</p>
                    <p className="text-sm text-gray-500">
                      {item.quantity} x {formatCurrency(item.price)}
                    </p>
                  </div>
                  <p className="font-medium text-gray-900">
                    {formatCurrency(item.quantity * item.price)}
                  </p>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex justify-between items-center">
                <p className="font-medium text-gray-900">Total</p>
                <p className="text-xl font-bold text-gray-900">
                  {formatCurrency(order.total)}
                </p>
              </div>
            </div>
          </div>
        </Card>

        <Card>
          <div className="p-4">
            <h4 className="text-sm font-medium text-gray-500 mb-2">
              Informações Adicionais
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-500">Status</p>
                <Badge variant="success">{order.status}</Badge>
              </div>
              <div>
                <p className="text-sm text-gray-500">Forma de Pagamento</p>
                <p className="font-medium text-gray-900">{order.paymentMethod}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Data do Pedido</p>
                <p className="font-medium text-gray-900">
                  {formatDateTime(order.createdAt)}
                </p>
              </div>
            </div>
          </div>
        </Card>

        <div className="flex justify-end space-x-2">
          <Button
            variant="secondary"
            onClick={onClose}
          >
            Fechar
          </Button>
          <Button
            onClick={onPrint}
          >
            Imprimir
          </Button>
        </div>
      </div>
    </Modal>
  );
}; 