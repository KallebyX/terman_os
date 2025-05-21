import React from 'react';
import { Form } from '../../../components/shared/Form';
import { User } from '../../../types';

interface ProfileFormProps {
  onSubmit: (data: Partial<User>) => void;
  initialValues: Partial<User>;
  isLoading?: boolean;
}

export const ProfileForm: React.FC<ProfileFormProps> = ({
  onSubmit,
  initialValues,
  isLoading
}) => {
  const fields = [
    { name: 'name', label: 'Nome completo', required: true },
    { name: 'email', label: 'E-mail', type: 'email', required: true },
    { name: 'phone', label: 'Telefone' },
    { name: 'document', label: 'CPF/CNPJ' },
    { name: 'currentPassword', label: 'Senha atual', type: 'password' },
    { name: 'newPassword', label: 'Nova senha', type: 'password' },
    { name: 'passwordConfirmation', label: 'Confirmar nova senha', type: 'password' }
  ];

  return (
    <Form
      fields={fields}
      onSubmit={onSubmit}
      initialValues={initialValues}
      isLoading={isLoading}
      submitText="Salvar alterações"
    />
  );
}; 