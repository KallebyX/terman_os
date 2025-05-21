import React from 'react';
import { formatCurrency, formatDateTime } from '../../utils/formatters';

interface ReceiptItem {
  name: string;
  quantity: number;
  price: number;
  total: number;
}

interface ReceiptProps {
  items: ReceiptItem[];
  total: number;
  paymentMethod: string;
  change?: number;
  date: Date;
  customerName?: string;
}

export const SaleReceipt: React.FC<ReceiptProps> = ({
  items,
  total,
  paymentMethod,
  change,
  date,
  customerName
}) => {
  return (
    <div className="p-4 font-mono text-sm">
      <div className="text-center mb-4">
        <h2 className="font-bold">COMPROVANTE DE VENDA</h2>
        <p>{formatDateTime(date)}</p>
      </div>

      {customerName && (
        <div className="mb-4">
          <p>Cliente: {customerName}</p>
        </div>
      )}

      <div className="border-t border-b border-gray-300 py-2 mb-4">
        {items.map((item, index) => (
          <div key={index} className="flex justify-between">
            <div>
              <p>{item.name}</p>
              <p className="text-xs text-gray-600">
                {item.quantity} x {formatCurrency(item.price)}
              </p>
            </div>
            <p>{formatCurrency(item.total)}</p>
          </div>
        ))}
      </div>

      <div className="space-y-2">
        <div className="flex justify-between font-bold">
          <p>TOTAL</p>
          <p>{formatCurrency(total)}</p>
        </div>
        <div className="flex justify-between">
          <p>Forma de Pagamento</p>
          <p>{paymentMethod}</p>
        </div>
        {change !== undefined && change > 0 && (
          <div className="flex justify-between">
            <p>Troco</p>
            <p>{formatCurrency(change)}</p>
          </div>
        )}
      </div>

      <div className="text-center mt-8 text-xs">
        <p>Obrigado pela preferência!</p>
      </div>
    </div>
  );
}; 