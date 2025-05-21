import React, { useState } from 'react';
import { Card, DateRangePicker } from '../ui';
import { LineChart } from '../charts';
import { useClientOrders } from '../../hooks/useClientOrders';
import { formatCurrency } from '../../utils/formatters';

export const ClientOrdersReport: React.FC = () => {
  const [dateRange, setDateRange] = useState<{ start: Date; end: Date }>();
  const { data, loading } = useClientOrders(dateRange);

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Histórico de Pedidos</h2>
        <DateRangePicker
          value={dateRange}
          onChange={setDateRange}
          className="w-72"
        />
      </div>

      {loading ? (
        <div>Carregando...</div>
      ) : (
        <div className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Total Gasto</p>
              <p className="text-2xl font-bold mt-1">{formatCurrency(data?.totalSpent || 0)}</p>
            </div>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500">Total de Pedidos</p>
              <p className="text-2xl font-bold mt-1">{data?.totalOrders || 0}</p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium mb-4">Histórico de Compras</h3>
            <div className="h-64">
              <LineChart data={data?.orderHistory || { labels: [], datasets: [] }} />
            </div>
          </div>

          <div>
            <h3 className="text-lg font-medium mb-4">Últimos Pedidos</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-3">Data</th>
                    <th className="text-left py-3">Pedido</th>
                    <th className="text-right py-3">Valor</th>
                    <th className="text-right py-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data?.recentOrders?.map((order) => (
                    <tr key={order.id} className="border-b">
                      <td className="py-3">{new Date(order.date).toLocaleDateString()}</td>
                      <td className="py-3">#{order.number}</td>
                      <td className="text-right py-3">{formatCurrency(order.total)}</td>
                      <td className="text-right py-3">
                        <span className={`px-2 py-1 rounded-full text-sm ${
                          order.status === 'completed' ? 'bg-green-100 text-green-800' :
                          order.status === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        }`}>
                          {order.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}; 