import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { SalesReportData } from '../types/reports';

interface UseSalesReportProps {
  start?: Date;
  end?: Date;
  groupBy?: 'day' | 'week' | 'month';
  category?: string;
}

export const useSalesReport = ({ start, end, groupBy = 'day', category }: UseSalesReportProps = {}) => {
  const [data, setData] = useState<SalesReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams({
          group_by: groupBy,
        });
        
        if (start) params.append('start_date', start.toISOString());
        if (end) params.append('end_date', end.toISOString());
        if (category) params.append('category', category);

        const response = await api.get('/reports/sales', { params });
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar relatório de vendas'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [start, end, groupBy, category]);

  return { data, loading, error };
}; 