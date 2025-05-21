import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { CustomerReportData } from '../types/reports';

interface UseCustomerReportProps {
  start?: Date;
  end?: Date;
  segment?: string;
  includeInactive?: boolean;
}

export const useCustomerReport = ({
  start,
  end,
  segment,
  includeInactive = false
}: UseCustomerReportProps = {}) => {
  const [data, setData] = useState<CustomerReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        
        if (start) params.append('start_date', start.toISOString());
        if (end) params.append('end_date', end.toISOString());
        if (segment) params.append('segment', segment);
        if (includeInactive) params.append('include_inactive', 'true');

        const response = await api.get('/reports/customers', { params });
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar relatório de clientes'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [start, end, segment, includeInactive]);

  return { data, loading, error };
}; 