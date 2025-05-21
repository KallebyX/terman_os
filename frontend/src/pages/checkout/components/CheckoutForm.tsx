import React from 'react';
import { Form } from '../../../components/shared/Form';

interface CheckoutFormProps {
  onSubmit: (data: any) => void;
  isLoading?: boolean;
}

export const CheckoutForm: React.FC<CheckoutFormProps> = ({
  onSubmit,
  isLoading
}) => {
  const fields = [
    { name: 'cardNumber', label: 'Número do Cartão', required: true },
    { name: 'cardName', label: 'Nome no Cartão', required: true },
    { name: 'expiryDate', label: 'Data de Validade', required: true },
    { name: 'cvv', label: 'CVV', required: true, type: 'password' },
    {
      name: 'installments',
      label: 'Parcelas',
      type: 'select',
      required: true,
      options: [
        { value: '1', label: '1x sem juros' },
        { value: '2', label: '2x sem juros' },
        { value: '3', label: '3x sem juros' }
      ]
    }
  ];

  return (
    <Form
      fields={fields}
      onSubmit={onSubmit}
      isLoading={isLoading}
      submitText="Finalizar Compra"
    />
  );
}; 