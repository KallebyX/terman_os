import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useAuth } from './useAuth';

interface ClientOrder {
  id: string;
  number: string;
  date: string;
  total: number;
  status: 'pending' | 'completed' | 'cancelled';
  items: Array<{
    id: string;
    product: string;
    quantity: number;
    price: number;
  }>;
}

interface ClientOrdersData {
  totalSpent: number;
  totalOrders: number;
  orderHistory: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
    }>;
  };
  recentOrders: ClientOrder[];
}

export const useClientOrders = (dateRange?: { start: Date; end: Date }) => {
  const [data, setData] = useState<ClientOrdersData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  const { user } = useAuth();

  useEffect(() => {
    const fetchOrders = async () => {
      if (!user) return;

      try {
        setLoading(true);
        const params = new URLSearchParams();
        
        if (dateRange?.start) params.append('start_date', dateRange.start.toISOString());
        if (dateRange?.end) params.append('end_date', dateRange.end.toISOString());

        const response = await api.get(`/client/orders`, { params });
        setData(response.data);
      } catch (err) {
        setError(err instanceof Error ? err : new Error('Erro ao carregar pedidos'));
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [user, dateRange]);

  return { data, loading, error };
}; 