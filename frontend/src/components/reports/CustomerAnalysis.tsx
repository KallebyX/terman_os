import React from 'react';
import { Card } from '../ui/Card';
import { Table, Thead, Tbody, Th, Td } from '../ui/Table';
import { formatCurrency } from '../../utils/formatters';

interface CustomerData {
  id: string;
  name: string;
  totalOrders: number;
  totalSpent: number;
  averageTicket: number;
  lastPurchase: string;
}

interface CustomerAnalysisProps {
  data: CustomerData[];
}

export const CustomerAnalysis: React.FC<CustomerAnalysisProps> = ({ data }) => {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-6">Análise de Clientes</h3>
      <Table>
        <Thead>
          <tr>
            <Th>Cliente</Th>
            <Th>Pedidos</Th>
            <Th>Total Gasto</Th>
            <Th>Ticket Médio</Th>
            <Th>Última Compra</Th>
          </tr>
        </Thead>
        <Tbody>
          {data.map(customer => (
            <tr key={customer.id}>
              <Td>{customer.name}</Td>
              <Td>{customer.totalOrders}</Td>
              <Td>{formatCurrency(customer.totalSpent)}</Td>
              <Td>{formatCurrency(customer.averageTicket)}</Td>
              <Td>
                {new Date(customer.lastPurchase).toLocaleDateString('pt-BR')}
              </Td>
            </tr>
          ))}
        </Tbody>
      </Table>
    </Card>
  );
}; 