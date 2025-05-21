import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { usePermissions } from './usePermissions';
import { ReportFilters } from '../types/reports';

interface AdminReportData {
  salesSummary: {
    daily: number;
    weekly: number;
    monthly: number;
    growth: number;
  };
  financialMetrics: {
    revenue: number;
    costs: number;
    profit: number;
    margin: number;
  };
  inventoryStatus: {
    totalItems: number;
    lowStock: number;
    outOfStock: number;
    value: number;
  };
  customerMetrics: {
    total: number;
    active: number;
    new: number;
    churnRate: number;
  };
}

export const useAdminReports = (filters?: ReportFilters) => {
  const [data, setData] = useState<AdminReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { canViewFinancials } = usePermissions();

  useEffect(() => {
    const fetchAdminReports = async () => {
      if (!canViewFinancials) {
        setError(new Error('Sem permissão para acessar relatórios administrativos'));
        return;
      }

      try {
        setLoading(true);
        const params = new URLSearchParams();
        
        if (filters?.dateRange) {
          params.append('start_date', filters.dateRange.start.toISOString());
          params.append('end_date', filters.dateRange.end.toISOString());
        }

        const response = await api.get('/admin/reports/summary', { params });
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar relatórios administrativos'));
      } finally {
        setLoading(false);
      }
    };

    fetchAdminReports();
  }, [canViewFinancials, filters]);

  return { data, loading, error };
}; 