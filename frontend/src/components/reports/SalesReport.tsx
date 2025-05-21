import React, { useState } from 'react';
import { Card, DateRangePicker, Select } from '../ui';
import { LineChart, BarChart } from '../charts';
import { useSalesReport } from '../../hooks/useSalesReport';
import { formatCurrency } from '../../utils/formatters';

interface SalesReportProps {
  initialDateRange?: { start: Date; end: Date };
}

export const SalesReport: React.FC<SalesReportProps> = ({ initialDateRange }) => {
  const [dateRange, setDateRange] = useState(initialDateRange);
  const [groupBy, setGroupBy] = useState<'day' | 'week' | 'month'>('day');
  const { data, loading, error } = useSalesReport(dateRange, groupBy);

  return (
    <Card className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Relatório de Vendas</h2>
        <div className="flex space-x-4">
          <DateRangePicker
            value={dateRange}
            onChange={setDateRange}
            className="w-72"
          />
          <Select
            value={groupBy}
            onChange={(value) => setGroupBy(value as 'day' | 'week' | 'month')}
            options={[
              { value: 'day', label: 'Diário' },
              { value: 'week', label: 'Semanal' },
              { value: 'month', label: 'Mensal' }
            ]}
            className="w-40"
          />
        </div>
      </div>

      {loading && <div>Carregando...</div>}
      {error && <div>Erro ao carregar dados</div>}
      
      {data && (
        <div className="space-y-8">
          <div className="grid grid-cols-3 gap-4">
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Total de Vendas</h3>
              <p className="text-2xl font-bold mt-2">{formatCurrency(data.totalSales)}</p>
              <p className={`text-sm mt-1 ${data.salesGrowth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.salesGrowth >= 0 ? '+' : ''}{data.salesGrowth}% vs período anterior
              </p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Ticket Médio</h3>
              <p className="text-2xl font-bold mt-2">{formatCurrency(data.averageTicket)}</p>
              <p className={`text-sm mt-1 ${data.ticketGrowth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.ticketGrowth >= 0 ? '+' : ''}{data.ticketGrowth}% vs período anterior
              </p>
            </Card>
            <Card className="p-4">
              <h3 className="text-sm text-gray-500">Total de Pedidos</h3>
              <p className="text-2xl font-bold mt-2">{data.totalOrders}</p>
              <p className={`text-sm mt-1 ${data.ordersGrowth >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                {data.ordersGrowth >= 0 ? '+' : ''}{data.ordersGrowth}% vs período anterior
              </p>
            </Card>
          </div>

          <div className="grid grid-cols-2 gap-6">
            <Card className="p-4">
              <h3 className="text-lg font-medium mb-4">Vendas por Período</h3>
              <LineChart
                data={data.salesByPeriod}
                xKey="period"
                yKey="value"
                height={300}
              />
            </Card>
            <Card className="p-4">
              <h3 className="text-lg font-medium mb-4">Top Produtos</h3>
              <BarChart
                data={data.topProducts}
                xKey="product"
                yKey="sales"
                height={300}
              />
            </Card>
          </div>

          <Card className="p-4">
            <h3 className="text-lg font-medium mb-4">Vendas por Categoria</h3>
            <div className="grid grid-cols-2 gap-6">
              <div>
                <BarChart
                  data={data.salesByCategory}
                  xKey="category"
                  yKey="value"
                  height={300}
                />
              </div>
              <div className="space-y-4">
                {data.salesByCategory.map((category) => (
                  <div key={category.category} className="flex justify-between items-center">
                    <div>
                      <p className="font-medium">{category.category}</p>
                      <p className="text-sm text-gray-500">{category.percentage}% das vendas</p>
                    </div>
                    <p className="font-bold">{formatCurrency(category.value)}</p>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      )}
    </Card>
  );
}; 