import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../components/ui/Toast';

interface OrderItem {
  id: string;
  productId: string;
  productName: string;
  quantity: number;
  price: number;
}

interface Order {
  id: string;
  customerId: string;
  customerName: string;
  items: OrderItem[];
  total: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  createdAt: string;
}

export const useOrders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const response = await api.get('/orders');
      setOrders(response.data);
    } catch (error) {
      addToast('Erro ao carregar pedidos', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const updateOrderStatus = async (id: string, status: Order['status']) => {
    try {
      const response = await api.put(`/orders/${id}/status`, { status });
      setOrders(prev => prev.map(o => o.id === id ? response.data : o));
      addToast('Status do pedido atualizado!', 'success');
      return response.data;
    } catch (error) {
      addToast('Erro ao atualizar status do pedido', 'error');
      throw error;
    }
  };

  return {
    orders,
    loading,
    updateOrderStatus,
    refetch: fetchOrders
  };
}; 