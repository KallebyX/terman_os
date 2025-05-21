import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { useInventory } from '../../hooks/useInventory';

export const StockAlerts: React.FC = () => {
  const { lowStockProducts, loading, updateStock } = useInventory();

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (lowStockProducts.length === 0) {
    return null;
  }

  return (
    <Card className="bg-yellow-50">
      <div className="p-4">
        <div className="flex items-center mb-4">
          <span className="material-icons text-yellow-500 mr-2">
            warning
          </span>
          <h3 className="text-lg font-medium text-yellow-800">
            Alertas de Estoque
          </h3>
        </div>

        <div className="space-y-4">
          {lowStockProducts.map(product => (
            <div
              key={product.id}
              className="flex items-center justify-between bg-white p-3 rounded-lg"
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
                onClick={() => {
                  // Implementar lógica de reposição de estoque
                }}
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