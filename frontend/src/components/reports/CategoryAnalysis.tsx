import React from 'react';
import { Card } from '../ui/Card';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { formatCurrency } from '../../utils/formatters';

interface CategoryData {
  name: string;
  value: number;
  percentage: number;
}

interface CategoryAnalysisProps {
  data: CategoryData[];
}

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899'];

export const CategoryAnalysis: React.FC<CategoryAnalysisProps> = ({ data }) => {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-6">Vendas por Categoria</h3>
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              cx="50%"
              cy="50%"
              outerRadius={100}
              label={({
                cx,
                cy,
                midAngle,
                innerRadius,
                outerRadius,
                percentage,
              }) => {
                const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
                const x = cx + radius * Math.cos(-midAngle * Math.PI / 180);
                const y = cy + radius * Math.sin(-midAngle * Math.PI / 180);
                return (
                  <text
                    x={x}
                    y={y}
                    fill="white"
                    textAnchor="middle"
                    dominantBaseline="central"
                  >
                    {`${percentage.toFixed(1)}%`}
                  </text>
                );
              }}
            >
              {data.map((entry, index) => (
                <Cell key={entry.name} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value: number) => formatCurrency(value)}
            />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-4 space-y-2">
        {data.map((category, index) => (
          <div key={category.name} className="flex justify-between items-center">
            <div className="flex items-center">
              <div
                className="w-3 h-3 rounded-full mr-2"
                style={{ backgroundColor: COLORS[index % COLORS.length] }}
              />
              <span className="text-sm text-gray-600">{category.name}</span>
            </div>
            <div className="text-sm font-medium">
              {formatCurrency(category.value)}
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}; 