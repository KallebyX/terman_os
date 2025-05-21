import React, { useEffect, useState } from 'react';
import { SalesChart } from '../../components/dashboard/SalesChart';
import { Card } from '../../components/ui/Card';
import { api } from '../../services/api';

interface DashboardData {
  totalSales: number;
  totalProducts: number;
  totalCustomers: number;
  salesByDay: Array<{ date: string; value: number }>;
}

export const DashboardPage: React.FC = () => {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get('/dashboard');
        setData(response.data);
      } catch (error) {
        console.error('Erro ao carregar dados do dashboard:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Carregando...</div>;
  if (!data) return <div>Erro ao carregar dados</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900">Total de Vendas</h3>
            <p className="mt-2 text-3xl font-bold">
              R$ {data.totalSales.toFixed(2)}
            </p>
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900">Produtos Cadastrados</h3>
            <p className="mt-2 text-3xl font-bold">{data.totalProducts}</p>
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <h3 className="text-lg font-medium text-gray-900">Total de Clientes</h3>
            <p className="mt-2 text-3xl font-bold">{data.totalCustomers}</p>
          </div>
        </Card>
      </div>

      <SalesChart
        data={data.salesByDay}
        title="Vendas por Dia"
      />
    </div>
  );
};
