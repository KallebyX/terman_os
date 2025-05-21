import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useToast } from '../../components/ui/Toast';
import { Form } from '../../components/form/Form';
import { FormField } from '../../components/form/FormField';
import { useForm } from '../../hooks/useForm';
import { validators } from '../../utils/validators';

interface LoginForm {
  email: string;
  password: string;
}

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { signIn } = useAuth();
  const { addToast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<LoginForm>({
    email: {
      value: '',
      rules: [validators.required, validators.email]
    },
    password: {
      value: '',
      rules: [validators.required, validators.minLength(6)]
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      await signIn(form.values.email, form.values.password);
      navigate('/app/dashboard');
    } catch (error) {
      addToast('Email ou senha inválidos', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-900 text-center mb-8">
        Login
      </h2>

      <Form
        onSubmit={handleSubmit}
        submitLabel="Entrar"
        isSubmitting={isSubmitting}
      >
        <FormField
          type="email"
          name="email"
          label="E-mail"
          value={form.values.email}
          onChange={(value) => form.handleChange('email', value)}
          error={form.touched.email ? form.errors.email : undefined}
          placeholder="seu@email.com"
        />

        <FormField
          type="password"
          name="password"
          label="Senha"
          value={form.values.password}
          onChange={(value) => form.handleChange('password', value)}
          error={form.touched.password ? form.errors.password : undefined}
          placeholder="••••••••"
        />

        <div className="flex items-center justify-between mt-4">
          <Link
            to="/forgot-password"
            className="text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            Esqueceu sua senha?
          </Link>
          <Link
            to="/register"
            className="text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            Criar conta
          </Link>
        </div>
      </Form>
    </div>
  );
}; 