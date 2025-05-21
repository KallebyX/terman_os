import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Select } from '../../components/ui/Select';
import { SalesChart } from '../../components/dashboard/SalesChart';
import { api } from '../../services/api';

interface ReportData {
  salesByPeriod: Array<{ date: string; value: number }>;
  topProducts: Array<{ name: string; total: number }>;
  topCustomers: Array<{ name: string; total: number }>;
}

export const ReportsPage: React.FC = () => {
  const [period, setPeriod] = useState('month');
  const [data, setData] = useState<ReportData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/reports?period=${period}`);
        setData(response.data);
      } catch (error) {
        console.error('Erro ao carregar relatórios:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [period]);

  if (loading) return <div>Carregando...</div>;
  if (!data) return <div>Erro ao carregar dados</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-900">Relatórios</h1>
        <Select
          options={[
            { value: 'week', label: 'Última Semana' },
            { value: 'month', label: 'Último Mês' },
            { value: 'year', label: 'Último Ano' }
          ]}
          value={period}
          onChange={e => setPeriod(e.target.value)}
        />
      </div>

      <SalesChart
        data={data.salesByPeriod}
        title="Vendas por Período"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Produtos Mais Vendidos
          </h3>
          <div className="space-y-4">
            {data.topProducts.map(product => (
              <div
                key={product.name}
                className="flex justify-between items-center"
              >
                <span className="text-gray-600">{product.name}</span>
                <span className="font-medium">
                  R$ {product.total.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <h3 className="text-lg font-medium text-gray-900 mb-4">
            Melhores Clientes
          </h3>
          <div className="space-y-4">
            {data.topCustomers.map(customer => (
              <div
                key={customer.name}
                className="flex justify-between items-center"
              >
                <span className="text-gray-600">{customer.name}</span>
                <span className="font-medium">
                  R$ {customer.total.toFixed(2)}
                </span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}; 