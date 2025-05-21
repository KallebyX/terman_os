import React from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';

interface ExportOptionsProps {
  onExport: (format: 'pdf' | 'csv') => void;
  isExporting?: boolean;
}

export const ExportOptions: React.FC<ExportOptionsProps> = ({
  onExport,
  isExporting = false
}) => {
  return (
    <Card className="p-6">
      <h3 className="text-lg font-medium text-gray-900 mb-4">
        Exportar Relatório
      </h3>
      <div className="flex space-x-4">
        <Button
          variant="secondary"
          onClick={() => onExport('pdf')}
          isLoading={isExporting}
        >
          Exportar PDF
        </Button>
        <Button
          variant="secondary"
          onClick={() => onExport('csv')}
          isLoading={isExporting}
        >
          Exportar CSV
        </Button>
      </div>
    </Card>
  );
}; 