import React from 'react';
import { Form } from '../../../components/shared/Form';
import { Product } from '../../../types';

interface ProductFormProps {
  onSubmit: (data: Partial<Product>) => void;
  initialValues?: Partial<Product>;
  isLoading?: boolean;
}

export const ProductForm: React.FC<ProductFormProps> = ({
  onSubmit,
  initialValues,
  isLoading
}) => {
  const fields = [
    { name: 'name', label: 'Nome', required: true },
    { name: 'code', label: 'Código', required: true },
    { name: 'description', label: 'Descrição', required: true },
    { name: 'price', label: 'Preço', type: 'number', required: true },
    { name: 'stock', label: 'Estoque', type: 'number', required: true },
    { name: 'category', label: 'Categoria', required: true },
    {
      name: 'status',
      label: 'Status',
      type: 'select',
      required: true,
      options: [
        { value: 'active', label: 'Ativo' },
        { value: 'inactive', label: 'Inativo' }
      ]
    }
  ];

  return (
    <Form
      fields={fields}
      onSubmit={onSubmit}
      initialValues={initialValues}
      isLoading={isLoading}
      submitText={initialValues ? 'Atualizar' : 'Cadastrar'}
    />
  );
}; 