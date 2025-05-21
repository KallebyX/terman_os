import React from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { formatCurrency } from '../../utils/formatters';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

interface CartSummaryProps {
  items: CartItem[];
  onUpdateQuantity: (id: string, quantity: number) => void;
  onRemoveItem: (id: string) => void;
  onFinalize: () => void;
  onClear: () => void;
  loading?: boolean;
}

export const CartSummary: React.FC<CartSummaryProps> = ({
  items,
  onUpdateQuantity,
  onRemoveItem,
  onFinalize,
  onClear,
  loading
}) => {
  const total = items.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  if (loading) {
    return (
      <Card className="h-full">
        <div className="p-4 space-y-4 animate-pulse">
          <div className="h-8 bg-gray-200 rounded" />
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-gray-200 rounded" />
            ))}
          </div>
          <div className="h-12 bg-gray-200 rounded" />
        </div>
      </Card>
    );
  }

  return (
    <Card className="h-full flex flex-col">
      <div className="p-4 flex-1">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900">
            Carrinho
          </h3>
          {items.length > 0 && (
            <Button
              variant="danger"
              size="sm"
              onClick={onClear}
            >
              Limpar
            </Button>
          )}
        </div>

        {items.length === 0 ? (
          <div className="text-center py-8">
            <span className="material-icons text-4xl text-gray-400">
              shopping_cart
            </span>
            <p className="text-gray-500 mt-2">
              Carrinho vazio
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {items.map(item => (
              <div
                key={item.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex-1">
                  <p className="font-medium text-gray-900 truncate">
                    {item.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {formatCurrency(item.price)}
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
                    ×
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="border-t border-gray-200 p-4">
        <div className="flex justify-between items-center mb-4">
          <span className="text-lg font-medium text-gray-900">Total</span>
          <span className="text-2xl font-bold text-gray-900">
            {formatCurrency(total)}
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