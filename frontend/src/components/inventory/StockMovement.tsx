import React, { useState } from 'react';
import { Modal } from '../ui/Modal';
import { Form } from '../form/Form';
import { FormField } from '../form/FormField';
import { useForm } from '../../hooks/useForm';
import { validators } from '../../utils/validators';

interface StockMovementProps {
  isOpen: boolean;
  onClose: () => void;
  productId: string;
  productName: string;
  currentStock: number;
  onConfirm: (quantity: number, type: 'add' | 'remove', reason: string) => Promise<void>;
}

export const StockMovement: React.FC<StockMovementProps> = ({
  isOpen,
  onClose,
  productId,
  productName,
  currentStock,
  onConfirm
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [type, setType] = useState<'add' | 'remove'>('add');

  const form = useForm({
    quantity: {
      value: '',
      rules: [
        validators.required,
        validators.numeric,
        (value) => {
          const num = Number(value);
          if (type === 'remove' && num > currentStock) {
            return 'Quantidade maior que o estoque atual';
          }
          return undefined;
        }
      ]
    },
    reason: {
      value: '',
      rules: [validators.required, validators.minLength(3)]
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      await onConfirm(
        Number(form.values.quantity),
        type,
        form.values.reason
      );
      onClose();
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Movimentação de Estoque"
    >
      <div className="mb-4">
        <p className="text-sm text-gray-600">Produto: {productName}</p>
        <p className="text-sm text-gray-600">Estoque atual: {currentStock}</p>
      </div>

      <Form
        onSubmit={handleSubmit}
        submitLabel="Confirmar"
        isSubmitting={isSubmitting}
        showCancel
        onCancel={onClose}
      >
        <FormField
          type="select"
          name="type"
          label="Tipo de Movimentação"
          value={type}
          onChange={setType}
          options={[
            { value: 'add', label: 'Entrada' },
            { value: 'remove', label: 'Saída' }
          ]}
        />

        <FormField
          type="number"
          name="quantity"
          label="Quantidade"
          value={form.values.quantity}
          onChange={(value) => form.handleChange('quantity', value)}
          error={form.touched.quantity ? form.errors.quantity : undefined}
        />

        <FormField
          type="text"
          name="reason"
          label="Motivo"
          value={form.values.reason}
          onChange={(value) => form.handleChange('reason', value)}
          error={form.touched.reason ? form.errors.reason : undefined}
        />
      </Form>
    </Modal>
  );
}; 