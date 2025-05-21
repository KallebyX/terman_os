import React from 'react';
import { Line } from 'react-chartjs-2';
import { Card } from '../../../components/ui';
import { formatCurrency } from '../../../utils/format';

interface SalesData {
  date: string;
  value: number;
}

interface SalesChartProps {
  data: SalesData[];
  period: 'day' | 'week' | 'month' | 'year';
}

export const SalesChart: React.FC<SalesChartProps> = ({ data, period }) => {
  const chartData = {
    labels: data.map(item => item.date),
    datasets: [
      {
        label: 'Vendas',
        data: data.map(item => item.value),
        fill: false,
        borderColor: 'rgb(59, 130, 246)',
        tension: 0.1
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: (context: any) => `Vendas: ${formatCurrency(context.raw)}`
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          callback: (value: number) => formatCurrency(value)
        }
      }
    }
  };

  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium mb-4">Vendas por {period}</h3>
      <Line data={chartData} options={options} />
    </Card>
  );
}; 