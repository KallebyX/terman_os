import React from 'react';
import { Card } from '../../../components/ui';
import { formatCurrency } from '../../../utils/format';

interface OrderItem {
  name: string;
  quantity: number;
  price: number;
}

interface OrderSummaryProps {
  items: OrderItem[];
}

export const OrderSummary: React.FC<OrderSummaryProps> = ({ items }) => {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const shipping = 0; // Implementar cálculo de frete
  const total = subtotal + shipping;

  return (
    <Card className="p-6">
      <h2 className="text-lg font-medium mb-4">Resumo do Pedido</h2>
      
      <div className="space-y-4">
        {items.map((item, index) => (
          <div key={index} className="flex justify-between">
            <span>
              {item.name} x {item.quantity}
            </span>
            <span>{formatCurrency(item.price * item.quantity)}</span>
          </div>
        ))}

        <div className="border-t pt-4">
          <div className="flex justify-between">
            <span>Subtotal</span>
            <span>{formatCurrency(subtotal)}</span>
          </div>
          <div className="flex justify-between">
            <span>Frete</span>
            <span>{shipping === 0 ? 'Grátis' : formatCurrency(shipping)}</span>
          </div>
          <div className="flex justify-between font-bold mt-2">
            <span>Total</span>
            <span>{formatCurrency(total)}</span>
          </div>
        </div>
      </div>
    </Card>
  );
}; 