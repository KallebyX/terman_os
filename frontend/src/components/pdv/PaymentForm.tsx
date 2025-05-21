import React, { useState } from 'react';
import { Modal } from '../ui/Modal';
import { Form } from '../form/Form';
import { FormField } from '../form/FormField';
import { useForm } from '../../hooks/useForm';
import { formatCurrency } from '../../utils/formatters';
import { validators } from '../../utils/validators';

interface PaymentFormProps {
  isOpen: boolean;
  onClose: () => void;
  total: number;
  onConfirm: (data: PaymentData) => void;
}

interface PaymentData {
  method: 'money' | 'credit' | 'debit' | 'pix';
  receivedAmount?: number;
  installments?: number;
}

export const PaymentForm: React.FC<PaymentFormProps> = ({
  isOpen,
  onClose,
  total,
  onConfirm
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm({
    method: {
      value: 'money',
      rules: [validators.required]
    },
    receivedAmount: {
      value: total,
      rules: [
        validators.required,
        (value) => Number(value) < total ? 'Valor recebido menor que o total' : undefined
      ]
    },
    installments: {
      value: 1,
      rules: []
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      await onConfirm({
        method: form.values.method as PaymentData['method'],
        receivedAmount: form.values.method === 'money' ? Number(form.values.receivedAmount) : undefined,
        installments: form.values.method === 'credit' ? Number(form.values.installments) : undefined
      });
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  const change = form.values.method === 'money' 
    ? Number(form.values.receivedAmount) - total 
    : 0;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Pagamento"
    >
      <div className="mb-6">
        <div className="text-center">
          <p className="text-lg text-gray-600">Total a pagar</p>
          <p className="text-3xl font-bold text-gray-900">
            {formatCurrency(total)}
          </p>
        </div>
      </div>

      <Form
        onSubmit={handleSubmit}
        submitLabel="Confirmar Pagamento"
        isSubmitting={isSubmitting}
        showCancel
        onCancel={onClose}
      >
        <FormField
          type="select"
          name="method"
          label="Forma de Pagamento"
          value={form.values.method}
          onChange={(value) => form.handleChange('method', value)}
          options={[
            { value: 'money', label: 'Dinheiro' },
            { value: 'credit', label: 'Cartão de Crédito' },
            { value: 'debit', label: 'Cartão de Débito' },
            { value: 'pix', label: 'PIX' }
          ]}
        />

        {form.values.method === 'money' && (
          <FormField
            type="number"
            name="receivedAmount"
            label="Valor Recebido"
            value={form.values.receivedAmount}
            onChange={(value) => form.handleChange('receivedAmount', value)}
            error={form.touched.receivedAmount ? form.errors.receivedAmount : undefined}
          />
        )}

        {form.values.method === 'credit' && (
          <FormField
            type="select"
            name="installments"
            label="Parcelas"
            value={form.values.installments}
            onChange={(value) => form.handleChange('installments', value)}
            options={Array.from({ length: 12 }, (_, i) => ({
              value: String(i + 1),
              label: `${i + 1}x ${i === 0 ? 'à vista' : ''}`
            }))}
          />
        )}

        {form.values.method === 'money' && change > 0 && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm font-medium text-gray-700">Troco</p>
            <p className="text-lg font-bold text-gray-900">
              {formatCurrency(change)}
            </p>
          </div>
        )}
      </Form>
    </Modal>
  );
}; 