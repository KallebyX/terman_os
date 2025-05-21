import { useState } from 'react';
import { api } from '../services/api';
import { usePermissions } from './usePermissions';
import { ReportFilters, ExportOptions } from '../types/reports';

export const useReportExport = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const { canExportReports } = usePermissions();

  const exportReport = async (
    reportType: string,
    filters?: ReportFilters,
    options?: ExportOptions
  ) => {
    if (!canExportReports) {
      throw new Error('Sem permissão para exportar relatórios');
    }

    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      if (filters?.dateRange) {
        params.append('start_date', filters.dateRange.start.toISOString());
        params.append('end_date', filters.dateRange.end.toISOString());
      }
      
      if (options) {
        params.append('format', options.format);
        if (options.includeCharts) params.append('include_charts', 'true');
        if (options.orientation) params.append('orientation', options.orientation);
      }

      const response = await api.get(`/reports/${reportType}/export`, {
        params,
        responseType: 'blob'
      });

      // Criar e disparar o download do arquivo
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${reportType}_report.${options?.format || 'pdf'}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Erro ao exportar relatório'));
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { exportReport, loading, error };
}; 