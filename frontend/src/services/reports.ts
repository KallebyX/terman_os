import { api } from './api';

interface SalesByPeriod {
  date: string;
  value: number;
}

interface TopProduct {
  id: string;
  name: string;
  total: number;
  quantity: number;
}

interface TopCustomer {
  id: string;
  name: string;
  total: number;
  ordersCount: number;
}

export const reportsService = {
  async getSalesByPeriod(period: 'day' | 'week' | 'month' | 'year'): Promise<SalesByPeriod[]> {
    const response = await api.get(`/reports/sales?period=${period}`);
    return response.data;
  },

  async getTopProducts(limit: number = 10): Promise<TopProduct[]> {
    const response = await api.get(`/reports/top-products?limit=${limit}`);
    return response.data;
  },

  async getTopCustomers(limit: number = 10): Promise<TopCustomer[]> {
    const response = await api.get(`/reports/top-customers?limit=${limit}`);
    return response.data;
  },

  async exportSalesReport(startDate: string, endDate: string, format: 'pdf' | 'csv'): Promise<Blob> {
    const response = await api.get(`/reports/export`, {
      params: { startDate, endDate, format },
      responseType: 'blob'
    });
    return response.data;
  }
}; 