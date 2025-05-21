import React from 'react';
import { Line, Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

interface ChartProps {
  type: 'line' | 'bar' | 'pie';
  data: any;
  options: any;
}

export const DashboardChart: React.FC<ChartProps> = ({ type, data, options }) => {
  const ChartComponent = {
    line: Line,
    bar: Bar,
    pie: Pie
  }[type];

  return (
    <div className="w-full h-64">
      <ChartComponent data={data} options={options} />
    </div>
  );
}; 