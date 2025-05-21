import React, { useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { AuthLayout } from './components/AuthLayout';
import { Form } from '../../components/shared/Form';
import { api } from '../../services/api';

export const ResetPasswordPage: React.FC = () => {
  const navigate = useNavigate();
  const { token } = useParams();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (data: { password: string; passwordConfirmation: string }) => {
    if (data.password !== data.passwordConfirmation) {
      setError('As senhas não coincidem');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      await api.post('/auth/reset-password', {
        token,
        password: data.password
      });

      navigate('/login', {
        state: { message: 'Senha alterada com sucesso! Faça login para continuar.' }
      });
    } catch (error: any) {
      setError(error.response?.data?.message || 'Erro ao redefinir senha');
    } finally {
      setIsLoading(false);
    }
  };

  const fields = [
    {
      name: 'password',
      label: 'Nova senha',
      type: 'password',
      required: true
    },
    {
      name: 'passwordConfirmation',
      label: 'Confirmar nova senha',
      type: 'password',
      required: true
    }
  ];

  return (
    <AuthLayout
      title="Redefinir senha"
      subtitle="Digite sua nova senha"
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
        submitText="Redefinir senha"
      />

      <div className="mt-6 text-sm">
        <Link
          to="/login"
          className="font-medium text-primary-600 hover:text-primary-500"
        >
          Voltar para o login
        </Link>
      </div>
    </AuthLayout>
  );
}; 