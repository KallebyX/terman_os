import { useState, useEffect } from 'react';
import { api } from '../services/api';
import { useToast } from '../components/ui/Toast';

interface Customer {
  id: string;
  name: string;
  email: string;
  phone: string;
  status: 'active' | 'inactive';
  createdAt: string;
}

export const useCustomers = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  const fetchCustomers = async () => {
    try {
      setLoading(true);
      const response = await api.get('/customers');
      setCustomers(response.data);
    } catch (error) {
      addToast('Erro ao carregar clientes', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const addCustomer = async (customer: Omit<Customer, 'id' | 'createdAt'>) => {
    try {
      const response = await api.post('/customers', customer);
      setCustomers(prev => [...prev, response.data]);
      addToast('Cliente adicionado com sucesso!', 'success');
      return response.data;
    } catch (error) {
      addToast('Erro ao adicionar cliente', 'error');
      throw error;
    }
  };

  const updateCustomer = async (id: string, data: Partial<Customer>) => {
    try {
      const response = await api.put(`/customers/${id}`, data);
      setCustomers(prev => prev.map(c => c.id === id ? response.data : c));
      addToast('Cliente atualizado com sucesso!', 'success');
      return response.data;
    } catch (error) {
      addToast('Erro ao atualizar cliente', 'error');
      throw error;
    }
  };

  const deleteCustomer = async (id: string) => {
    try {
      await api.delete(`/customers/${id}`);
      setCustomers(prev => prev.filter(c => c.id !== id));
      addToast('Cliente removido com sucesso!', 'success');
    } catch (error) {
      addToast('Erro ao remover cliente', 'error');
      throw error;
    }
  };

  return {
    customers,
    loading,
    addCustomer,
    updateCustomer,
    deleteCustomer,
    refetch: fetchCustomers
  };
}; 