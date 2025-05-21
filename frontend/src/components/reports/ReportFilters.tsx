import React from 'react';
import { Card } from '../ui/Card';
import { Select } from '../ui/Select';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

interface ReportFiltersProps {
  period: string;
  startDate: string;
  endDate: string;
  onPeriodChange: (period: string) => void;
  onStartDateChange: (date: string) => void;
  onEndDateChange: (date: string) => void;
  onGenerateReport: () => void;
  isLoading?: boolean;
}

export const ReportFilters: React.FC<ReportFiltersProps> = ({
  period,
  startDate,
  endDate,
  onPeriodChange,
  onStartDateChange,
  onEndDateChange,
  onGenerateReport,
  isLoading = false
}) => {
  return (
    <Card className="p-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Select
          label="Período"
          value={period}
          onChange={e => onPeriodChange(e.target.value)}
          options={[
            { value: 'today', label: 'Hoje' },
            { value: 'week', label: 'Última Semana' },
            { value: 'month', label: 'Último Mês' },
            { value: 'custom', label: 'Personalizado' }
          ]}
        />
        
        {period === 'custom' && (
          <>
            <Input
              type="date"
              label="Data Inicial"
              value={startDate}
              onChange={e => onStartDateChange(e.target.value)}
            />
            <Input
              type="date"
              label="Data Final"
              value={endDate}
              onChange={e => onEndDateChange(e.target.value)}
            />
          </>
        )}
        
        <div className="flex items-end">
          <Button
            onClick={onGenerateReport}
            isLoading={isLoading}
            fullWidth
          >
            Gerar Relatório
          </Button>
        </div>
      </div>
    </Card>
  );
}; 