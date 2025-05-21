import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { AuthLayout } from './components/AuthLayout';
import { Form } from '../../components/shared/Form';
import { api } from '../../services/api';

export const RegisterPage: React.FC = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    setError('');

    try {
      await api.post('/auth/register', data);
      navigate('/login', {
        state: { message: 'Cadastro realizado com sucesso! Faça login para continuar.' }
      });
    } catch (error: any) {
      setError(error.response?.data?.message || 'Erro ao realizar cadastro');
    } finally {
      setIsLoading(false);
    }
  };

  const fields = [
    {
      name: 'name',
      label: 'Nome completo',
      required: true
    },
    {
      name: 'email',
      label: 'E-mail',
      type: 'email',
      required: true
    },
    {
      name: 'password',
      label: 'Senha',
      type: 'password',
      required: true
    },
    {
      name: 'passwordConfirmation',
      label: 'Confirmar senha',
      type: 'password',
      required: true
    }
  ];

  return (
    <AuthLayout
      title="Criar nova conta"
      subtitle="Preencha os dados abaixo para começar"
    >
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      <Form
        fields={fields}
        onSubmit={handleSubmit}
        isLoading={isLoading}
        submitText="Cadastrar"
      />

      <div className="mt-6 text-sm">
        <Link
          to="/login"
          className="font-medium text-primary-600 hover:text-primary-500"
        >
          Já tem uma conta? Faça login
        </Link>
      </div>
    </AuthLayout>
  );
}; 