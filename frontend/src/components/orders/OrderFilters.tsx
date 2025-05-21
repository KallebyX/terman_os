import React from 'react';
import { Card } from '../ui/Card';
import { FormField } from '../form/FormField';
import { Button } from '../ui/Button';

interface OrderFiltersProps {
  filters: {
    status: string;
    startDate: string;
    endDate: string;
    search: string;
  };
  onFilterChange: (filters: any) => void;
  onClearFilters: () => void;
}

export const OrderFilters: React.FC<OrderFiltersProps> = ({
  filters,
  onFilterChange,
  onClearFilters
}) => {
  return (
    <Card>
      <div className="p-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <FormField
            type="select"
            name="status"
            label="Status"
            value={filters.status}
            onChange={(value) => onFilterChange({ ...filters, status: value })}
            options={[
              { value: '', label: 'Todos' },
              { value: 'pending', label: 'Pendente' },
              { value: 'processing', label: 'Em Processamento' },
              { value: 'completed', label: 'Concluído' },
              { value: 'cancelled', label: 'Cancelado' }
            ]}
          />

          <FormField
            type="date"
            name="startDate"
            label="Data Inicial"
            value={filters.startDate}
            onChange={(value) => onFilterChange({ ...filters, startDate: value })}
          />

          <FormField
            type="date"
            name="endDate"
            label="Data Final"
            value={filters.endDate}
            onChange={(value) => onFilterChange({ ...filters, endDate: value })}
          />

          <FormField
            type="text"
            name="search"
            label="Buscar"
            value={filters.search}
            onChange={(value) => onFilterChange({ ...filters, search: value })}
            placeholder="Buscar por cliente ou pedido"
          />
        </div>

        <div className="mt-4 flex justify-end">
          <Button
            variant="secondary"
            onClick={onClearFilters}
          >
            Limpar Filtros
          </Button>
        </div>
      </div>
    </Card>
  );
}; 