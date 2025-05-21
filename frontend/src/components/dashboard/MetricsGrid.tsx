import React from 'react';
import { Card } from '../ui/Card';
import { formatCurrency } from '../../utils/formatters';

interface Metric {
  label: string;
  value: number;
  trend?: {
    value: number;
    isPositive: boolean;
  };
  icon?: React.ReactNode;
  type: 'currency' | 'number' | 'percentage';
}

interface MetricsGridProps {
  metrics: Metric[];
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ metrics }) => {
  const formatValue = (value: number, type: Metric['type']) => {
    switch (type) {
      case 'currency':
        return formatCurrency(value);
      case 'percentage':
        return `${value.toFixed(1)}%`;
      default:
        return value.toLocaleString('pt-BR');
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <Card key={index} className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">
                {metric.label}
              </p>
              <p className="mt-2 text-3xl font-semibold text-gray-900">
                {formatValue(metric.value, metric.type)}
              </p>
              {metric.trend && (
                <div className="mt-2 flex items-center">
                  <span
                    className={`text-sm font-medium ${
                      metric.trend.isPositive ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {metric.trend.isPositive ? '+' : '-'}
                    {metric.trend.value}%
                  </span>
                  <span className="ml-2 text-sm text-gray-500">
                    vs. período anterior
                  </span>
                </div>
              )}
            </div>
            {metric.icon && (
              <div className="p-3 bg-blue-50 rounded-full">
                {metric.icon}
              </div>
            )}
          </div>
        </Card>
      ))}
    </div>
  );
}; 