import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { InventoryReportData } from '../types/reports';

interface UseInventoryReportProps {
  category?: string;
  location?: string;
  includeInactive?: boolean;
}

export const useInventoryReport = ({ 
  category,
  location,
  includeInactive = false 
}: UseInventoryReportProps = {}) => {
  const [data, setData] = useState<InventoryReportData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        
        if (category) params.append('category', category);
        if (location) params.append('location', location);
        if (includeInactive) params.append('include_inactive', 'true');

        const response = await api.get('/reports/inventory', { params });
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar relatório de estoque'));
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [category, location, includeInactive]);

  return { data, loading, error };
}; 