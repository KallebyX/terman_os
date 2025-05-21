import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import { ChartData } from '../../types/reports';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface BarChartProps {
  data: ChartData;
  height?: number;
  title?: string;
  showLegend?: boolean;
  yAxisLabel?: string;
  xAxisLabel?: string;
  stacked?: boolean;
}

export const BarChart: React.FC<BarChartProps> = ({
  data,
  height = 300,
  title,
  showLegend = true,
  yAxisLabel,
  xAxisLabel,
  stacked = false
}) => {
  const options: ChartOptions<'bar'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: showLegend,
        position: 'top' as const,
      },
      title: {
        display: !!title,
        text: title
      },
    },
    scales: {
      y: {
        stacked,
        beginAtZero: true,
        title: {
          display: !!yAxisLabel,
          text: yAxisLabel
        }
      },
      x: {
        stacked,
        title: {
          display: !!xAxisLabel,
          text: xAxisLabel
        }
      }
    }
  };

  return (
    <div style={{ height }}>
      <Bar data={data} options={options} />
    </div>
  );
}; 