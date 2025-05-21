import React from 'react';
import { Product } from '../../types/common';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';

interface CartItem extends Product {
  quantity: number;
}

interface CartProps {
  items: CartItem[];
  onUpdateQuantity: (productId: string, quantity: number) => void;
  onRemoveItem: (productId: string) => void;
  onFinalize: () => void;
}

export const Cart: React.FC<CartProps> = ({
  items,
  onUpdateQuantity,
  onRemoveItem,
  onFinalize
}) => {
  const total = items.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  return (
    <Card className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto">
        {items.map(item => (
          <div
            key={item.id}
            className="flex items-center justify-between py-4 border-b border-gray-200 last:border-0"
          >
            <div className="flex-1">
              <h4 className="text-sm font-medium text-gray-900">
                {item.name}
              </h4>
              <p className="text-sm text-gray-500">
                R$ {item.price.toFixed(2)}
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                disabled={item.quantity <= 1}
              >
                -
              </Button>
              <span className="w-8 text-center">{item.quantity}</span>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
              >
                +
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => onRemoveItem(item.id)}
              >
                X
              </Button>
            </div>
          </div>
        ))}
      </div>
      <div className="border-t border-gray-200 pt-4">
        <div className="flex justify-between mb-4">
          <span className="text-lg font-medium">Total:</span>
          <span className="text-lg font-medium">
            R$ {total.toFixed(2)}
          </span>
        </div>
        <Button
          fullWidth
          onClick={onFinalize}
          disabled={items.length === 0}
        >
          Finalizar Venda
        </Button>
      </div>
    </Card>
  );
}; 