import React from 'react';
import { Form } from '../../../components/shared/Form';
import { Customer } from '../../../types';

interface CustomerFormProps {
  onSubmit: (data: Partial<Customer>) => void;
  initialValues?: Partial<Customer>;
  isLoading?: boolean;
}

export const CustomerForm: React.FC<CustomerFormProps> = ({
  onSubmit,
  initialValues,
  isLoading
}) => {
  const fields = [
    { name: 'name', label: 'Nome', required: true },
    { name: 'email', label: 'E-mail', type: 'email', required: true },
    { name: 'phone', label: 'Telefone', required: true },
    { name: 'document', label: 'CPF/CNPJ', required: true },
    { name: 'address.street', label: 'Rua', required: true },
    { name: 'address.number', label: 'Número', required: true },
    { name: 'address.complement', label: 'Complemento' },
    { name: 'address.neighborhood', label: 'Bairro', required: true },
    { name: 'address.city', label: 'Cidade', required: true },
    { name: 'address.state', label: 'Estado', required: true },
    { name: 'address.zipcode', label: 'CEP', required: true }
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