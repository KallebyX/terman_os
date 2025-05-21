import React from 'react';
import { Card } from '../../../components/ui';

interface KPIData {
  value: string | number;
  change?: string;
  positive?: boolean;
}

interface KPICardProps {
  title: string;
  data: KPIData;
  icon: string;
  iconBgColor: string;
  iconColor: string;
  dateRange: 'week' | 'month' | 'year';
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  data,
  icon,
  iconBgColor,
  iconColor,
  dateRange
}) => {
  const periodText = {
    week: 'esta semana',
    month: 'este mês',
    year: 'este ano'
  };

  return (
    <Card variant="elevated" className="p-6">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-secondary-500 text-sm mb-1">{title}</p>
          <h3 className="text-2xl font-bold mb-1">{data.value || 'N/A'}</h3>
          {data.change && (
            <p className={`text-sm ${data.positive ? 'text-green-500' : 'text-red-500'}`}>
              <i className={`fas fa-arrow-${data.positive ? 'up' : 'down'} mr-1`}></i>
              {data.change} {periodText[dateRange]}
            </p>
          )}
        </div>
        <div className={`${iconBgColor} p-3 rounded-full ${iconColor}`}>
          <i className={`fas fa-${icon} text-xl`}></i>
        </div>
      </div>
    </Card>
  );
}; 