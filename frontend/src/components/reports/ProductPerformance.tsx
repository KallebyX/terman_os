import React from 'react';
import { Card } from '../ui/Card';
import { Table, Thead, Tbody, Th, Td } from '../ui/Table';
import { Badge } from '../ui/Badge';
import { formatCurrency } from '../../utils/formatters';

interface ProductData {
  id: string;
  name: string;
  totalSold: number;
  revenue: number;
  stock: number;
  status: 'low' | 'medium' | 'high';
}

interface ProductPerformanceProps {
  data: ProductData[];
}

export const ProductPerformance: React.FC<ProductPerformanceProps> = ({ data }) => {
  const getStatusBadge = (status: ProductData['status']) => {
    switch (status) {
      case 'low':
        return <Badge variant="danger">Baixo</Badge>;
      case 'medium':
        return <Badge variant="warning">Médio</Badge>;
      case 'high':
        return <Badge variant="success">Alto</Badge>;
    }
  };

  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-6">
        Desempenho de Produtos
      </h3>
      <Table>
        <Thead>
          <tr>
            <Th>Produto</Th>
            <Th>Vendidos</Th>
            <Th>Receita</Th>
            <Th>Estoque</Th>
            <Th>Desempenho</Th>
          </tr>
        </Thead>
        <Tbody>
          {data.map(product => (
            <tr key={product.id}>
              <Td>{product.name}</Td>
              <Td>{product.totalSold}</Td>
              <Td>{formatCurrency(product.revenue)}</Td>
              <Td>{product.stock}</Td>
              <Td>{getStatusBadge(product.status)}</Td>
            </tr>
          ))}
        </Tbody>
      </Table>
    </Card>
  );
}; 