import { useState, useCallback } from 'react';
import { saleService } from '../services/saleService';
import { customerService } from '../services/customerService';
import { productService } from '../services/productService';
import { useToast } from '../components/ui/Toast';

interface ReportParams {
  period: 'day' | 'week' | 'month' | 'year';
  startDate?: string;
  endDate?: string;
}

export const useReports = () => {
  const [loading, setLoading] = useState(false);
  const [salesData, setSalesData] = useState(null);
  const [topCustomers, setTopCustomers] = useState([]);
  const [topProducts, setTopProducts] = useState([]);
  const { addToast } = useToast();

  const generateReport = useCallback(async (params: ReportParams) => {
    try {
      setLoading(true);
      const [sales, customers, products] = await Promise.all([
        saleService.getReportData(params),
        customerService.getTopCustomers(),
        productService.list()
      ]);

      setSalesData(sales);
      setTopCustomers(customers);
      setTopProducts(products);
    } catch (error) {
      addToast('Erro ao gerar relatório', 'error');
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  const exportReport = async (format: 'pdf' | 'csv', params: ReportParams) => {
    try {
      setLoading(true);
      const response = await saleService.exportReport(format, params);
      
      // Criar blob e fazer download
      const blob = new Blob([response.data], { 
        type: format === 'pdf' ? 'application/pdf' : 'text/csv' 
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `relatorio_${new Date().toISOString()}.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      addToast('Relatório exportado com sucesso!', 'success');
    } catch (error) {
      addToast('Erro ao exportar relatório', 'error');
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    salesData,
    topCustomers,
    topProducts,
    generateReport,
    exportReport
  };
}; 