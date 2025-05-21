import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

interface StockAlertProduct {
  id: string;
  name: string;
  stock: number;
  minStock: number;
}

interface StockAlertProps {
  products: StockAlertProduct[];
  onReplenish: (productId: string) => void;
}

export const StockAlert: React.FC<StockAlertProps> = ({
  products,
  onReplenish
}) => {
  if (products.length === 0) return null;

  return (
    <Card className="bg-yellow-50 border-yellow-100">
      <div className="p-4">
        <div className="flex items-center mb-4">
          <span className="material-icons text-yellow-500 mr-2">
            warning
          </span>
          <h3 className="text-lg font-medium text-yellow-800">
            Alertas de Estoque
          </h3>
        </div>

        <div className="space-y-3">
          {products.map(product => (
            <div
              key={product.id}
              className="flex items-center justify-between"
            >
              <div>
                <p className="font-medium text-gray-900">{product.name}</p>
                <div className="flex items-center space-x-2 mt-1">
                  <Badge variant="warning">
                    Estoque: {product.stock}
                  </Badge>
                  <Badge variant="danger">
                    Mínimo: {product.minStock}
                  </Badge>
                </div>
              </div>
              <Button
                variant="secondary"
                size="sm"
                onClick={() => onReplenish(product.id)}
              >
                Repor Estoque
              </Button>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}; 