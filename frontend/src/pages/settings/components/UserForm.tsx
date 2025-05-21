import React from 'react';
import { Form } from '../../../components/shared/Form';

interface UserFormProps {
  onSubmit: (data: any) => void;
  initialValues?: any;
  isLoading?: boolean;
}

export const UserForm: React.FC<UserFormProps> = ({
  onSubmit,
  initialValues,
  isLoading
}) => {
  const fields = [
    { name: 'name', label: 'Nome', required: true },
    { name: 'email', label: 'E-mail', type: 'email', required: true },
    {
      name: 'role',
      label: 'Função',
      type: 'select',
      required: true,
      options: [
        { value: 'admin', label: 'Administrador' },
        { value: 'manager', label: 'Gerente' },
        { value: 'employee', label: 'Funcionário' }
      ]
    },
    {
      name: 'status',
      label: 'Status',
      type: 'select',
      required: true,
      options: [
        { value: 'active', label: 'Ativo' },
        { value: 'inactive', label: 'Inativo' }
      ]
    },
    ...(!initialValues ? [
      { name: 'password', label: 'Senha', type: 'password', required: true },
      { name: 'passwordConfirmation', label: 'Confirmar Senha', type: 'password', required: true }
    ] : [])
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