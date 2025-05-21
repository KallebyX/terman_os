import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Card } from '../../../components/ui';

interface ProductData {
  name: string;
  quantity: number;
}

interface ProductsChartProps {
  data: ProductData[];
  title: string;
}

export const ProductsChart: React.FC<ProductsChartProps> = ({ data, title }) => {
  const chartData = {
    labels: data.map(item => item.name),
    datasets: [
      {
        label: 'Quantidade',
        data: data.map(item => item.quantity),
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
        borderColor: 'rgb(59, 130, 246)',
        borderWidth: 1
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1
        }
      }
    }
  };

  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium mb-4">{title}</h3>
      <Bar data={chartData} options={options} />
    </Card>
  );
}; 