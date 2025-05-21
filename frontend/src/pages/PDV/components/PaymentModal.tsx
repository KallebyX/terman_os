import React from 'react';
import { Modal, Button } from '../../../components/ui';

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  paymentMethod: string;
  onPaymentMethodChange: (method: string) => void;
  total: number;
}

export const PaymentModal: React.FC<PaymentModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  paymentMethod,
  onPaymentMethodChange,
  total
}) => {
  const paymentMethods = [
    'Dinheiro',
    'Cartão de Crédito',
    'Cartão de Débito',
    'PIX'
  ];

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Finalizar Venda">
      <div className="space-y-4">
        <div>
          <h3 className="text-lg font-medium">Forma de Pagamento</h3>
          <div className="mt-2 space-y-2">
            {paymentMethods.map((method) => (
              <div key={method} className="flex items-center">
                <input
                  type="radio"
                  id={method}
                  name="paymentMethod"
                  value={method}
                  checked={paymentMethod === method}
                  onChange={(e) => onPaymentMethodChange(e.target.value)}
                  className="mr-2"
                />
                <label htmlFor={method}>{method}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="border-t pt-4">
          <div className="flex justify-between items-center">
            <span className="text-lg font-medium">Total a pagar:</span>
            <span className="text-2xl font-bold">
              {new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
              }).format(total)}
            </span>
          </div>
        </div>

        <div className="flex justify-end space-x-2">
          <Button variant="outline" onClick={onClose}>
            Cancelar
          </Button>
          <Button
            variant="primary"
            onClick={onConfirm}
            disabled={!paymentMethod}
          >
            Confirmar Pagamento
          </Button>
        </div>
      </div>
    </Modal>
  );
}; 