import React, { useState } from 'react';
import { Form } from '../../../components/shared/Form';
import { api } from '../../../services/api';

export const Contact: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    try {
      await api.post('/contact', data);
      setSuccess(true);
    } catch (error) {
      alert('Erro ao enviar mensagem. Tente novamente.');
    } finally {
      setIsLoading(false);
    }
  };

  const fields = [
    { name: 'name', label: 'Nome', required: true },
    { name: 'email', label: 'E-mail', type: 'email', required: true },
    { name: 'phone', label: 'Telefone' },
    { name: 'company', label: 'Empresa' },
    { name: 'message', label: 'Mensagem', type: 'textarea', required: true }
  ];

  return (
    <div className="bg-white py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900">
            Entre em contato
          </h2>
          <p className="mt-4 text-lg text-gray-500">
            Tire suas dúvidas e saiba mais sobre nossos planos
          </p>
        </div>

        <div className="mt-12 max-w-lg mx-auto">
          {success ? (
            <div className="text-center">
              <i className="fas fa-check-circle text-5xl text-green-500 mb-4" />
              <h3 className="text-xl font-medium text-gray-900">
                Mensagem enviada com sucesso!
              </h3>
              <p className="mt-2 text-gray-500">
                Entraremos em contato em breve.
              </p>
            </div>
          ) : (
            <Form
              fields={fields}
              onSubmit={handleSubmit}
              isLoading={isLoading}
              submitText="Enviar mensagem"
            />
          )}
        </div>
      </div>
    </div>
  );
}; 