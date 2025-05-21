import React from 'react';
import { Input, Button } from '../../../components/ui';

interface OrderFiltersProps {
  filters: {
    status: string;
    dateRange: {
      start: string;
      end: string;
    };
    search: string;
  };
  onFilterChange: (filters: any) => void;
}

export const OrderFilters: React.FC<OrderFiltersProps> = ({
  filters,
  onFilterChange
}) => {
  const statusOptions = [
    { value: '', label: 'Todos' },
    { value: 'pending', label: 'Pendente' },
    { value: 'processing', label: 'Em Processamento' },
    { value: 'completed', label: 'Concluído' },
    { value: 'cancelled', label: 'Cancelado' }
  ];

  return (
    <div className="bg-white p-4 rounded-lg shadow mb-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Status</label>
          <select
            value={filters.status}
            onChange={(e) => onFilterChange({ ...filters, status: e.target.value })}
            className="form-select w-full"
          >
            {statusOptions.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Data Inicial</label>
          <Input
            type="date"
            value={filters.dateRange.start}
            onChange={(e) => onFilterChange({
              ...filters,
              dateRange: { ...filters.dateRange, start: e.target.value }
            })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Data Final</label>
          <Input
            type="date"
            value={filters.dateRange.end}
            onChange={(e) => onFilterChange({
              ...filters,
              dateRange: { ...filters.dateRange, end: e.target.value }
            })}
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Buscar</label>
          <Input
            type="text"
            placeholder="Buscar pedidos..."
            value={filters.search}
            onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
          />
        </div>
      </div>
    </div>
  );
}; 