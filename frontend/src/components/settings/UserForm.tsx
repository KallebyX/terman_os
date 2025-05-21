import React, { useState } from 'react';
import { Form } from '../form/Form';
import { FormField } from '../form/FormField';
import { useForm } from '../../hooks/useForm';
import { validators } from '../../utils/validators';

interface UserFormProps {
  initialData?: {
    name: string;
    email: string;
    role: string;
    status: string;
  };
  onSubmit: (data: any) => Promise<void>;
  onCancel: () => void;
}

export const UserForm: React.FC<UserFormProps> = ({
  initialData,
  onSubmit,
  onCancel
}) => {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm({
    name: {
      value: initialData?.name || '',
      rules: [validators.required, validators.minLength(3)]
    },
    email: {
      value: initialData?.email || '',
      rules: [validators.required, validators.email]
    },
    role: {
      value: initialData?.role || 'seller',
      rules: [validators.required]
    },
    status: {
      value: initialData?.status || 'active',
      rules: [validators.required]
    },
    password: {
      value: '',
      rules: initialData ? [] : [validators.required, validators.minLength(6)]
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      const data = { ...form.values };
      if (!data.password) delete data.password;
      await onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Form
      onSubmit={handleSubmit}
      submitLabel={initialData ? 'Atualizar' : 'Criar'}
      isSubmitting={isSubmitting}
      showCancel
      onCancel={onCancel}
    >
      <FormField
        type="text"
        name="name"
        label="Nome"
        value={form.values.name}
        onChange={(value) => form.handleChange('name', value)}
        error={form.touched.name ? form.errors.name : undefined}
      />

      <FormField
        type="email"
        name="email"
        label="E-mail"
        value={form.values.email}
        onChange={(value) => form.handleChange('email', value)}
        error={form.touched.email ? form.errors.email : undefined}
      />

      <FormField
        type="select"
        name="role"
        label="Função"
        value={form.values.role}
        onChange={(value) => form.handleChange('role', value)}
        options={[
          { value: 'admin', label: 'Administrador' },
          { value: 'manager', label: 'Gerente' },
          { value: 'seller', label: 'Vendedor' }
        ]}
      />

      <FormField
        type="select"
        name="status"
        label="Status"
        value={form.values.status}
        onChange={(value) => form.handleChange('status', value)}
        options={[
          { value: 'active', label: 'Ativo' },
          { value: 'inactive', label: 'Inativo' }
        ]}
      />

      {!initialData && (
        <FormField
          type="password"
          name="password"
          label="Senha"
          value={form.values.password}
          onChange={(value) => form.handleChange('password', value)}
          error={form.touched.password ? form.errors.password : undefined}
        />
      )}
    </Form>
  );
}; 