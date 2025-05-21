import React from 'react';
import { Card } from '../ui/Card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { formatCurrency } from '../../utils/formatters';

interface SalesData {
  date: string;
  revenue: number;
  orders: number;
  averageTicket: number;
}

interface SalesAnalyticsProps {
  data: SalesData[];
  period: 'day' | 'week' | 'month' | 'year';
}

export const SalesAnalytics: React.FC<SalesAnalyticsProps> = ({ data, period }) => {
  const formatXAxis = (date: string) => {
    const d = new Date(date);
    switch (period) {
      case 'day':
        return d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
      case 'week':
        return d.toLocaleDateString('pt-BR', { weekday: 'short' });
      case 'month':
        return d.toLocaleDateString('pt-BR', { day: '2-digit' });
      case 'year':
        return d.toLocaleDateString('pt-BR', { month: 'short' });
    }
  };

  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-6">Análise de Vendas</h3>
      <div className="h-96">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              tickFormatter={formatXAxis}
            />
            <YAxis
              yAxisId="left"
              tickFormatter={(value) => formatCurrency(value)}
            />
            <YAxis
              yAxisId="right"
              orientation="right"
              tickFormatter={(value) => value.toFixed(0)}
            />
            <Tooltip
              formatter={(value: any, name: string) => {
                switch (name) {
                  case 'revenue':
                    return [formatCurrency(value), 'Receita'];
                  case 'orders':
                    return [value, 'Pedidos'];
                  case 'averageTicket':
                    return [formatCurrency(value), 'Ticket Médio'];
                  default:
                    return [value, name];
                }
              }}
            />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="revenue"
              stroke="#3B82F6"
              name="Receita"
            />
            <Line
              yAxisId="right"
              type="monotone"
              dataKey="orders"
              stroke="#10B981"
              name="Pedidos"
            />
            <Line
              yAxisId="left"
              type="monotone"
              dataKey="averageTicket"
              stroke="#F59E0B"
              name="Ticket Médio"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}; 