import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { FinancialReportData } from '../types/reports';

interface UseFinancialReportProps {
  start?: Date;
  end?: Date;
}

export const useFinancialReport = ({ start, end }: UseFinancialReportProps = {}) => {
  const [data, setData] = useState<FinancialReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (start) params.append('start_date', start.toISOString());
        if (end) params.append('end_date', end.toISOString());

        const response = await api.get('/reports/financial', { params });
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar relatório financeiro'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [start, end]);

  return { data, loading, error };
}; 