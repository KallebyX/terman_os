import { useState, useEffect, useCallback } from 'react';
import { saleService } from '../services/saleService';
import { useToast } from '../components/ui/Toast';

export const useSales = (initialParams?: {
  startDate?: string;
  endDate?: string;
  status?: string;
  customerId?: string;
}) => {
  const [sales, setSales] = useState([]);
  const [loading, setLoading] = useState(true);
  const [params, setParams] = useState(initialParams);
  const { addToast } = useToast();

  const fetchSales = useCallback(async () => {
    try {
      setLoading(true);
      const data = await saleService.list(params);
      setSales(data);
    } catch (error) {
      addToast('Erro ao carregar vendas', 'error');
    } finally {
      setLoading(false);
    }
  }, [params, addToast]);

  useEffect(() => {
    fetchSales();
  }, [fetchSales]);

  const createSale = async (saleData: any) => {
    try {
      const newSale = await saleService.create(saleData);
      setSales(prev => [...prev, newSale]);
      addToast('Venda realizada com sucesso!', 'success');
      return newSale;
    } catch (error) {
      addToast('Erro ao realizar venda', 'error');
      throw error;
    }
  };

  const updateSaleStatus = async (id: string, status: string) => {
    try {
      const updatedSale = await saleService.updateStatus(id, status);
      setSales(prev => prev.map(sale => 
        sale.id === id ? updatedSale : sale
      ));
      addToast('Status atualizado com sucesso!', 'success');
      return updatedSale;
    } catch (error) {
      addToast('Erro ao atualizar status', 'error');
      throw error;
    }
  };

  const cancelSale = async (id: string, reason: string) => {
    try {
      const canceledSale = await saleService.cancel(id, reason);
      setSales(prev => prev.map(sale => 
        sale.id === id ? canceledSale : sale
      ));
      addToast('Venda cancelada com sucesso!', 'success');
      return canceledSale;
    } catch (error) {
      addToast('Erro ao cancelar venda', 'error');
      throw error;
    }
  };

  return {
    sales,
    loading,
    params,
    setParams,
    createSale,
    updateSaleStatus,
    cancelSale,
    refetch: fetchSales
  };
}; 