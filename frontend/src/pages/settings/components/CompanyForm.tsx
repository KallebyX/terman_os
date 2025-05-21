import React from 'react';
import { Form } from '../../../components/shared/Form';

interface CompanyFormProps {
  onSubmit: (data: any) => void;
  initialValues: any;
  isLoading?: boolean;
}

export const CompanyForm: React.FC<CompanyFormProps> = ({
  onSubmit,
  initialValues,
  isLoading
}) => {
  const fields = [
    { name: 'name', label: 'Nome da Empresa', required: true },
    { name: 'document', label: 'CNPJ', required: true },
    { name: 'email', label: 'E-mail', type: 'email', required: true },
    { name: 'phone', label: 'Telefone', required: true },
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
      submitText="Salvar"
    />
  );
}; 