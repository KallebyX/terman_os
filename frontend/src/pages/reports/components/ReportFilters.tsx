import React from 'react';
import { Button } from '../../../components/ui';

interface ReportFiltersProps {
  period: string;
  onPeriodChange: (period: string) => void;
  onExport: () => void;
}

export const ReportFilters: React.FC<ReportFiltersProps> = ({
  period,
  onPeriodChange,
  onExport
}) => {
  const periods = [
    { value: 'day', label: 'Hoje' },
    { value: 'week', label: 'Esta Semana' },
    { value: 'month', label: 'Este Mês' },
    { value: 'year', label: 'Este Ano' }
  ];

  return (
    <div className="flex items-center justify-between mb-6">
      <div className="flex space-x-2">
        {periods.map(({ value, label }) => (
          <Button
            key={value}
            variant={period === value ? 'primary' : 'outline'}
            onClick={() => onPeriodChange(value)}
          >
            {label}
          </Button>
        ))}
      </div>
      <Button onClick={onExport} leftIcon={<i className="fas fa-download" />}>
        Exportar
      </Button>
    </div>
  );
}; 