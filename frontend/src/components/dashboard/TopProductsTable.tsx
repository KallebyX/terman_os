import React from 'react';
import { Card } from '../ui/Card';
import { Table, Thead, Tbody, Th, Td } from '../ui/Table';
import { formatCurrency } from '../../utils/formatters';

interface TopProduct {
  id: string;
  name: string;
  quantity: number;
  revenue: number;
}

interface TopProductsTableProps {
  products: TopProduct[];
}

export const TopProductsTable: React.FC<TopProductsTableProps> = ({ products }) => {
  return (
    <Card>
      <div className="p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Produtos Mais Vendidos
        </h3>
        <Table>
          <Thead>
            <tr>
              <Th>Produto</Th>
              <Th>Quantidade</Th>
              <Th>Receita</Th>
            </tr>
          </Thead>
          <Tbody>
            {products.map(product => (
              <tr key={product.id}>
                <Td>{product.name}</Td>
                <Td>{product.quantity}</Td>
                <Td>{formatCurrency(product.revenue)}</Td>
              </tr>
            ))}
          </Tbody>
        </Table>
      </div>
    </Card>
  );
}; 