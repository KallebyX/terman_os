import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useToast } from '../../components/ui/Toast';
import { Form } from '../../components/form/Form';
import { FormField } from '../../components/form/FormField';
import { useForm } from '../../hooks/useForm';
import { validators } from '../../utils/validators';
import { authService } from '../../services/auth';

interface ForgotPasswordForm {
  email: string;
}

export const ForgotPasswordPage: React.FC = () => {
  const { addToast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [emailSent, setEmailSent] = useState(false);

  const form = useForm<ForgotPasswordForm>({
    email: {
      value: '',
      rules: [validators.required, validators.email]
    }
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.validateForm()) return;

    try {
      setIsSubmitting(true);
      await authService.forgotPassword(form.values.email);
      setEmailSent(true);
      addToast('Email de recuperação enviado com sucesso!', 'success');
    } catch (error) {
      addToast('Erro ao enviar email de recuperação', 'error');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (emailSent) {
    return (
      <div className="text-center">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          Email Enviado!
        </h2>
        <p className="text-gray-600 mb-6">
          Verifique sua caixa de entrada e siga as instruções para redefinir sua senha.
        </p>
        <Link
          to="/login"
          className="text-blue-600 hover:text-blue-500 font-medium"
        >
          Voltar para o login
        </Link>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-3xl font-bold text-gray-900 text-center mb-4">
        Recuperar Senha
      </h2>
      <p className="text-gray-600 text-center mb-8">
        Digite seu e-mail e enviaremos as instruções para redefinir sua senha.
      </p>

      <Form
        onSubmit={handleSubmit}
        submitLabel="Enviar"
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

        <div className="text-center mt-4">
          <Link
            to="/login"
            className="text-sm font-medium text-blue-600 hover:text-blue-500"
          >
            Voltar para o login
          </Link>
        </div>
      </Form>
    </div>
  );
}; 