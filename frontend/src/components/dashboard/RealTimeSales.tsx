import React, { useEffect, useState } from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { formatCurrency, formatDateTime } from '../../utils/formatters';
import { api } from '../../config/api';

interface SaleEvent {
  id: string;
  total: number;
  items: number;
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: string;
}

export const RealTimeSales: React.FC = () => {
  const [sales, setSales] = useState<SaleEvent[]>([]);

  useEffect(() => {
    const eventSource = new EventSource(`${api.defaults.baseURL}/events/sales`);

    eventSource.onmessage = (event) => {
      const sale = JSON.parse(event.data);
      setSales(prev => [sale, ...prev].slice(0, 10));
    };

    return () => {
      eventSource.close();
    };
  }, []);

  const getStatusBadge = (status: SaleEvent['status']) => {
    switch (status) {
      case 'completed':
        return <Badge variant="success">Concluída</Badge>;
      case 'pending':
        return <Badge variant="warning">Pendente</Badge>;
      case 'cancelled':
        return <Badge variant="danger">Cancelada</Badge>;
    }
  };

  return (
    <Card>
      <div className="p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">
          Vendas em Tempo Real
        </h3>
        <div className="space-y-4">
          {sales.length === 0 ? (
            <p className="text-gray-500 text-center py-4">
              Aguardando novas vendas...
            </p>
          ) : (
            sales.map(sale => (
              <div
                key={sale.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-medium">#{sale.id.slice(-6)}</span>
                    {getStatusBadge(sale.status)}
                  </div>
                  <p className="text-sm text-gray-500 mt-1">
                    {formatDateTime(sale.createdAt)}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-medium text-gray-900">
                    {formatCurrency(sale.total)}
                  </p>
                  <p className="text-sm text-gray-500">
                    {sale.items} {sale.items === 1 ? 'item' : 'itens'}
                  </p>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </Card>
  );
}; 