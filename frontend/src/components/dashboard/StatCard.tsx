import React from 'react';
import { Card } from '../ui/Card';
import { formatCurrency } from '../../utils/formatters';

interface StatCardProps {
  title: string;
  value: number | string;
  icon?: React.ReactNode;
  type?: 'currency' | 'number' | 'text';
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  type = 'text',
  trend
}) => {
  const formatValue = () => {
    if (type === 'currency') return formatCurrency(Number(value));
    if (type === 'number') return Number(value).toLocaleString('pt-BR');
    return value;
  };

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="mt-2 text-3xl font-semibold text-gray-900">
            {formatValue()}
          </p>
          {trend && (
            <div className="mt-2 flex items-center">
              <span
                className={`text-sm font-medium ${
                  trend.isPositive ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {trend.isPositive ? '+' : '-'}{trend.value}%
              </span>
              <span className="ml-2 text-sm text-gray-500">vs. mês anterior</span>
            </div>
          )}
        </div>
        {icon && (
          <div className="p-3 bg-blue-50 rounded-full">
            {icon}
          </div>
        )}
      </div>
    </Card>
  );
}; 