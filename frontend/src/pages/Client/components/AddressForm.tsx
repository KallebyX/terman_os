import React from 'react';
import { Form } from '../../../components/shared/Form';
import { Address } from '../../../types';

interface AddressFormProps {
  onSubmit: (data: Partial<Address>) => void;
  initialValues?: Partial<Address>;
  isLoading?: boolean;
}

export const AddressForm: React.FC<AddressFormProps> = ({
  onSubmit,
  initialValues,
  isLoading
}) => {
  const fields = [
    { name: 'name', label: 'Nome do endereço', required: true },
    { name: 'zipcode', label: 'CEP', required: true },
    { name: 'street', label: 'Rua', required: true },
    { name: 'number', label: 'Número', required: true },
    { name: 'complement', label: 'Complemento' },
    { name: 'neighborhood', label: 'Bairro', required: true },
    { name: 'city', label: 'Cidade', required: true },
    {
      name: 'state',
      label: 'Estado',
      type: 'select',
      required: true,
      options: [
        { value: 'AC', label: 'Acre' },
        { value: 'AL', label: 'Alagoas' },
        // ... outros estados
      ]
    }
  ];

  return (
    <Form
      fields={fields}
      onSubmit={onSubmit}
      initialValues={initialValues}
      isLoading={isLoading}
      submitText={initialValues ? 'Atualizar' : 'Adicionar'}
    />
  );
}; 