import React from 'react';
import { Card } from '../ui';
import { TrendIndicator } from './TrendIndicator';
import { formatCurrency, formatPercentage } from '../../utils/formatters';

interface MetricCardProps {
  title: string;
  value: number;
  previousValue?: number;
  type?: 'currency' | 'percentage' | 'number';
  icon?: React.ReactNode;
  className?: string;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  previousValue,
  type = 'number',
  icon,
  className
}) => {
  const formatValue = (val: number) => {
    switch (type) {
      case 'currency':
        return formatCurrency(val);
      case 'percentage':
        return formatPercentage(val);
      default:
        return new Intl.NumberFormat('pt-BR').format(val);
    }
  };

  const calculateGrowth = () => {
    if (!previousValue) return null;
    return ((value - previousValue) / previousValue) * 100;
  };

  const growth = calculateGrowth();

  return (
    <Card className={`p-4 ${className}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-gray-500">{title}</span>
        {icon && <div className="text-gray-400">{icon}</div>}
      </div>
      <div className="flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold">{formatValue(value)}</p>
          {growth !== null && (
            <div className="flex items-center mt-1">
              <TrendIndicator value={growth} />
              <span className="text-sm ml-1">vs período anterior</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
}; 