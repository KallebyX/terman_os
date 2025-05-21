import React, { useState } from 'react';
import { Card, Select, Button } from '../ui';
import { useInventoryReport } from '../../hooks/useInventoryReport';
import { formatCurrency } from '../../utils/formatters';

export const InventoryReport: React.FC = () => {
  const [category, setCategory] = useState<string>('all');
  const { data, loading, error } = useInventoryReport(category);

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Relatório de Estoque</h2>
        <div className="flex space-x-4">
          <Select
            value={category}
            onChange={(value) => setCategory(value)}
            options={[
              { value: 'all', label: 'Todas Categorias' },
              // Adicionar categorias dinâmicas aqui
            ]}
            className="w-48"
          />
          <Button variant="outline" onClick={() => {}}>
            Exportar PDF
          </Button>
        </div>
      </div>

      {loading && <div>Carregando...</div>}
      {error && <div>Erro ao carregar dados</div>}

      {data && (
        <div className="space-y-6">
          <div className="grid grid-cols-4 gap-4">
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Valor Total em Estoque</h3>
              <p className="text-2xl font-bold mt-2">{formatCurrency(data.totalValue)}</p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Itens em Estoque</h3>
              <p className="text-2xl font-bold mt-2">{data.totalItems}</p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Itens Abaixo do Mínimo</h3>
              <p className="text-2xl font-bold mt-2 text-red-600">{data.lowStockItems}</p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Giro de Estoque</h3>
              <p className="text-2xl font-bold mt-2">{data.turnoverRate}x</p>
            </Card>
          </div>

          <Card className="p-4">
            <h3 className="text-lg font-medium mb-4">Produtos com Estoque Crítico</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3">Produto</th>
                    <th className="text-left py-3">Código</th>
                    <th className="text-right py-3">Em Estoque</th>
                    <th className="text-right py-3">Mínimo</th>
                    <th className="text-right py-3">Sugestão de Compra</th>
                  </tr>
                </thead>
                <tbody>
                  {data.criticalItems.map((item) => (
                    <tr key={item.id} className="border-b">
                      <td className="py-3">{item.name}</td>
                      <td className="py-3">{item.code}</td>
                      <td className="text-right py-3 text-red-600">{item.currentStock}</td>
                      <td className="text-right py-3">{item.minStock}</td>
                      <td className="text-right py-3">{item.suggestedPurchase}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          <div className="grid grid-cols-2 gap-6">
            <Card className="p-4">
              <h3 className="text-lg font-medium mb-4">Produtos Mais Vendidos</h3>
              <div className="space-y-4">
                {data.topSellingProducts.map((product) => (
                  <div key={product.id} className="flex justify-between items-center">
                    <div>
                      <p className="font-medium">{product.name}</p>
                      <p className="text-sm text-gray-500">{product.category}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold">{product.soldQuantity} un.</p>
                      <p className="text-sm text-gray-500">Em estoque: {product.currentStock}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>

            <Card className="p-4">
              <h3 className="text-lg font-medium mb-4">Produtos Parados</h3>
              <div className="space-y-4">
                {data.nonMovingProducts.map((product) => (
                  <div key={product.id} className="flex justify-between items-center">
                    <div>
                      <p className="font-medium">{product.name}</p>
                      <p className="text-sm text-gray-500">Último movimento: {product.lastMovement}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold">{product.currentStock} un.</p>
                      <p className="text-sm text-gray-500">{formatCurrency(product.stockValue)}</p>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        </div>
      )}
    </Card>
  );
}; 