import { api } from '../config/api';

interface SaleItem {
  productId: string;
  quantity: number;
  price: number;
}

interface Sale {
  id: string;
  items: SaleItem[];
  customerId?: string;
  total: number;
  paymentMethod: string;
  status: string;
  createdAt: string;
}

export const saleService = {
  async create(data: Omit<Sale, 'id' | 'createdAt'>) {
    const response = await api.post('/sales', data);
    return response.data;
  },

  async list(params?: {
    startDate?: string;
    endDate?: string;
    status?: string;
    customerId?: string;
  }) {
    const response = await api.get('/sales', { params });
    return response.data;
  },

  async getById(id: string) {
    const response = await api.get(`/sales/${id}`);
    return response.data;
  },

  async updateStatus(id: string, status: string) {
    const response = await api.put(`/sales/${id}/status`, { status });
    return response.data;
  },

  async cancel(id: string, reason: string) {
    const response = await api.post(`/sales/${id}/cancel`, { reason });
    return response.data;
  },

  async getDashboardData() {
    const response = await api.get('/sales/dashboard');
    return response.data;
  },

  async getReportData(params: {
    period: 'day' | 'week' | 'month' | 'year';
    startDate?: string;
    endDate?: string;
  }) {
    const response = await api.get('/sales/report', { params });
    return response.data;
  }
}; 