import React, { useState } from 'react';
import { OrderFilters } from './components/OrderFilters';
import { OrderList } from './components/OrderList';
import { OrderDetails } from './components/OrderDetails';
import { LoadingSpinner } from '../../components/shared/LoadingSpinner';
import { ErrorMessage } from '../../components/shared/ErrorMessage';
import { useOrders } from '../../hooks/useOrders';
import { Order } from '../../types';

export const OrderManagementPage: React.FC = () => {
  const { orders, isLoading, error, updateOrderStatus } = useOrders();
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);
  const [filters, setFilters] = useState({
    status: '',
    dateRange: {
      start: '',
      end: ''
    },
    search: ''
  });

  const filteredOrders = orders.filter(order => {
    const matchesStatus = !filters.status || order.status === filters.status;
    const matchesSearch = !filters.search ||
      order.customer.name.toLowerCase().includes(filters.search.toLowerCase()) ||
      order.id.toString().includes(filters.search);
    const matchesDateRange = (!filters.dateRange.start || new Date(order.created_at) >= new Date(filters.dateRange.start)) &&
      (!filters.dateRange.end || new Date(order.created_at) <= new Date(filters.dateRange.end));

    return matchesStatus && matchesSearch && matchesDateRange;
  });

  const handleUpdateStatus = async (orderId: number, status: Order['status']) => {
    try {
      await updateOrderStatus(orderId, status);
    } catch (error: any) {
      alert(error.message);
    }
  };

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">Gerenciamento de Pedidos</h1>

      <OrderFilters
        filters={filters}
        onFilterChange={setFilters}
      />

      <OrderList
        orders={filteredOrders}
        onViewDetails={setSelectedOrder}
        onUpdateStatus={handleUpdateStatus}
      />

      <OrderDetails
        order={selectedOrder}
        isOpen={!!selectedOrder}
        onClose={() => setSelectedOrder(null)}
      />
    </div>
  );
};

export default OrderManagementPage;
