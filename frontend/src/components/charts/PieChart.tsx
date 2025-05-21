import React from 'react';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';
import { Pie } from 'react-chartjs-2';
import { ChartData } from '../../types/reports';

ChartJS.register(ArcElement, Tooltip, Legend);

interface PieChartProps {
  data: ChartData;
  height?: number;
  title?: string;
  showLegend?: boolean;
  donut?: boolean;
}

export const PieChart: React.FC<PieChartProps> = ({
  data,
  height = 300,
  title,
  showLegend = true,
  donut = false
}) => {
  const options: ChartOptions<'pie'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: showLegend,
        position: 'right' as const,
      },
      title: {
        display: !!title,
        text: title
      },
    },
    cutout: donut ? '50%' : undefined
  };

  return (
    <div style={{ height }}>
      <Pie data={data} options={options} />
    </div>
  );
}; 