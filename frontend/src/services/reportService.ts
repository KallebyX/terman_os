import { api } from './api';
import {
  FinancialReportData,
  SalesReportData,
  InventoryReportData,
  CustomerReportData,
  ReportFilters,
  ExportOptions
} from '../types/reports';

export const reportService = {
  async getFinancialReport(filters?: ReportFilters): Promise<FinancialReportData> {
    const params = new URLSearchParams();
    
    if (filters?.dateRange) {
      params.append('start_date', filters.dateRange.start.toISOString());
      params.append('end_date', filters.dateRange.end.toISOString());
    }
    
    const response = await api.get('/reports/financial', { params });
    return response.data;
  },

  async getSalesReport(filters?: ReportFilters): Promise<SalesReportData> {
    const params = new URLSearchParams();
    
    if (filters?.dateRange) {
      params.append('start_date', filters.dateRange.start.toISOString());
      params.append('end_date', filters.dateRange.end.toISOString());
    }
    if (filters?.groupBy) params.append('group_by', filters.groupBy);
    if (filters?.category) params.append('category', filters.category);
    if (filters?.paymentMethod) params.append('payment_method', filters.paymentMethod);
    
    const response = await api.get('/reports/sales', { params });
    return response.data;
  },

  async getInventoryReport(filters?: ReportFilters): Promise<InventoryReportData> {
    const params = new URLSearchParams();
    
    if (filters?.category) params.append('category', filters.category);
    if (filters?.location) params.append('location', filters.location);
    if (filters?.includeInactive) params.append('include_inactive', 'true');
    
    const response = await api.get('/reports/inventory', { params });
    return response.data;
  },

  async getCustomerReport(filters?: ReportFilters): Promise<CustomerReportData> {
    const params = new URLSearchParams();
    
    if (filters?.dateRange) {
      params.append('start_date', filters.dateRange.start.toISOString());
      params.append('end_date', filters.dateRange.end.toISOString());
    }
    if (filters?.segment) params.append('segment', filters.segment);
    if (filters?.includeInactive) params.append('include_inactive', 'true');
    
    const response = await api.get('/reports/customers', { params });
    return response.data;
  },

  async exportReport(
    reportType: 'financial' | 'sales' | 'inventory' | 'customers',
    filters?: ReportFilters,
    options?: ExportOptions
  ): Promise<Blob> {
    const params = new URLSearchParams();
    
    if (filters?.dateRange) {
      params.append('start_date', filters.dateRange.start.toISOString());
      params.append('end_date', filters.dateRange.end.toISOString());
    }
    if (filters?.groupBy) params.append('group_by', filters.groupBy);
    if (filters?.category) params.append('category', filters.category);
    if (filters?.segment) params.append('segment', filters.segment);
    if (filters?.location) params.append('location', filters.location);
    
    if (options) {
      params.append('format', options.format);
      if (options.includeCharts) params.append('include_charts', 'true');
      if (options.orientation) params.append('orientation', options.orientation);
      if (options.detailed) params.append('detailed', 'true');
    }
    
    const response = await api.get(`/reports/${reportType}/export`, {
      params,
      responseType: 'blob'
    });
    
    return response.data;
  },

  async getRealtimeMetrics(): Promise<{
    onlineUsers: number;
    cartAbandonment: number;
    conversionRate: number;
    activeSessions: number;
  }> {
    const response = await api.get('/reports/realtime-metrics');
    return response.data;
  },

  async getDashboardAlerts(): Promise<{
    lowStock: Array<{ product: string; currentStock: number; minStock: number }>;
    paymentFailures: Array<{ orderId: string; amount: number; reason: string }>;
    systemAlerts: Array<{ message: string; severity: string; timestamp: string }>;
  }> {
    const response = await api.get('/reports/dashboard-alerts');
    return response.data;
  },

  async getCustomReportData(
    metrics: string[],
    filters?: ReportFilters
  ): Promise<Record<string, any>> {
    const params = new URLSearchParams();
    
    params.append('metrics', metrics.join(','));
    
    if (filters?.dateRange) {
      params.append('start_date', filters.dateRange.start.toISOString());
      params.append('end_date', filters.dateRange.end.toISOString());
    }
    if (filters?.groupBy) params.append('group_by', filters.groupBy);
    
    const response = await api.get('/reports/custom', { params });
    return response.data;
  }
};

// Utilitários para processamento de dados dos relatórios
export const reportUtils = {
  calculateGrowth(current: number, previous: number): number {
    if (previous === 0) return 0;
    return ((current - previous) / previous) * 100;
  },

  formatCurrency(value: number): string {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  },

  formatPercentage(value: number): string {
    return new Intl.NumberFormat('pt-BR', {
      style: 'percent',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value / 100);
  },

  groupDataByPeriod(data: any[], dateField: string, valueField: string, period: 'day' | 'week' | 'month'): any[] {
    const grouped = data.reduce((acc, item) => {
      const date = new Date(item[dateField]);
      let key: string;

      switch (period) {
        case 'week':
          key = `${date.getFullYear()}-W${Math.ceil((date.getDate() + date.getDay()) / 7)}`;
          break;
        case 'month':
          key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
          break;
        default: // day
          key = date.toISOString().split('T')[0];
      }

      if (!acc[key]) {
        acc[key] = { period: key, value: 0, count: 0 };
      }

      acc[key].value += item[valueField];
      acc[key].count += 1;

      return acc;
    }, {});

    return Object.values(grouped);
  }
}; 