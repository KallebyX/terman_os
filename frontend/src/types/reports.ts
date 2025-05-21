export interface FinancialReportData {
  totalRevenue: number;
  netProfit: number;
  profitMargin: number;
  operationalCosts: number;
  revenueGrowth: number;
  profitGrowth: number;
  profitMarginGoal: number;
  costsPercentage: number;
  revenueVsExpenses: Array<{
    date: string;
    revenue: number;
    expenses: number;
  }>;
  expenseDistribution: Array<{
    name: string;
    value: number;
    percentage: number;
  }>;
  revenueByCategory: Array<{
    name: string;
    value: number;
    percentage: number;
  }>;
  paymentMethods: Array<{
    name: string;
    value: number;
    percentage: number;
  }>;
  topExpenses: Array<{
    category: string;
    value: number;
    percentage: number;
    growth: number;
  }>;
  dailyCashFlow: Array<{
    date: string;
    inflow: number;
    outflow: number;
    balance: number;
  }>;
  currentBalance: number;
  accountsReceivable: number;
  accountsPayable: number;
}

// Continuando com mais tipos... Quer que eu prossiga? 

export interface SalesReportData {
  totalSales: number;
  averageTicket: number;
  totalOrders: number;
  salesGrowth: number;
  ticketGrowth: number;
  ordersGrowth: number;
  salesByPeriod: Array<{
    period: string;
    value: number;
    quantity: number;
    orders: number;
  }>;
  topProducts: Array<{
    id: string;
    name: string;
    quantity: number;
    revenue: number;
    growth: number;
  }>;
  salesByCategory: Array<{
    category: string;
    value: number;
    percentage: number;
    growth: number;
  }>;
  salesByPaymentMethod: Array<{
    method: string;
    value: number;
    percentage: number;
  }>;
  salesByHour: Array<{
    hour: number;
    value: number;
    orders: number;
  }>;
  salesByDayOfWeek: Array<{
    day: string;
    value: number;
    orders: number;
  }>;
}

export interface InventoryReportData {
  totalValue: number;
  totalItems: number;
  lowStockItems: number;
  turnoverRate: number;
  criticalItems: Array<{
    id: string;
    name: string;
    code: string;
    currentStock: number;
    minStock: number;
    suggestedPurchase: number;
    lastPurchaseDate: string;
    averageDailySales: number;
  }>;
  topSellingProducts: Array<{
    id: string;
    name: string;
    category: string;
    soldQuantity: number;
    currentStock: number;
    turnoverRate: number;
  }>;
  nonMovingProducts: Array<{
    id: string;
    name: string;
    currentStock: number;
    lastMovement: string;
    stockValue: number;
    daysWithoutMovement: number;
  }>;
  stockByCategory: Array<{
    category: string;
    itemCount: number;
    totalValue: number;
    percentage: number;
  }>;
  stockMovement: Array<{
    date: string;
    inbound: number;
    outbound: number;
    balance: number;
  }>;
}

export interface CustomerReportData {
  totalCustomers: number;
  activeCustomers: number;
  newCustomers: number;
  customerGrowth: number;
  averageLifetimeValue: number;
  customerSegments: Array<{
    segment: string;
    count: number;
    percentage: number;
    averageTicket: number;
    totalRevenue: number;
  }>;
  topCustomers: Array<{
    id: string;
    name: string;
    totalPurchases: number;
    totalSpent: number;
    lastPurchase: string;
    segment: string;
  }>;
  customerRetention: {
    rate: number;
    byMonth: Array<{
      month: string;
      rate: number;
      activeCustomers: number;
      churnedCustomers: number;
    }>;
  };
  purchaseFrequency: Array<{
    frequency: string;
    customerCount: number;
    percentage: number;
  }>;
  customerSatisfaction: {
    averageRating: number;
    totalReviews: number;
    ratingDistribution: Array<{
      rating: number;
      count: number;
      percentage: number;
    }>;
  };
}

export interface DashboardData {
  summary: {
    dailySales: number;
    dailyOrders: number;
    averageTicket: number;
    activeCustomers: number;
  };
  trends: {
    salesGrowth: number;
    ordersGrowth: number;
    customerGrowth: number;
    profitGrowth: number;
  };
  realtimeMetrics: {
    onlineUsers: number;
    cartAbandonment: number;
    conversionRate: number;
  };
  alerts: Array<{
    type: 'low_stock' | 'payment_failed' | 'high_demand' | 'system';
    message: string;
    severity: 'low' | 'medium' | 'high';
    timestamp: string;
  }>;
}

export interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    backgroundColor?: string | string[];
    borderColor?: string;
    borderWidth?: number;
  }>;
}

export interface ReportFilters {
  dateRange?: {
    start: Date;
    end: Date;
  };
  groupBy?: 'hour' | 'day' | 'week' | 'month' | 'year';
  category?: string;
  segment?: string;
  location?: string;
  includeInactive?: boolean;
  paymentMethod?: string;
}

export interface ExportOptions {
  format: 'pdf' | 'excel' | 'csv';
  includeCharts?: boolean;
  orientation?: 'portrait' | 'landscape';
  detailed?: boolean;
} 